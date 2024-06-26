import streamlit as st
from color_palettes import color_palette_names
from background_generator import art_styles_list, art_shapes_list, Canvas
from color_palettes import color_palettes, color_palette_names
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from streamlit_card import card
import requests
from urllib.parse import quote
from random import choice
from PIL import Image
from io import BytesIO

load_dotenv()
spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

def selectIndex(index):
    st.session_state.selectedIndex = index

@st.cache_data(show_spinner=False, max_entries=1)
def searchSpotify(query):
    return spotify.search(searchQuery, type='track', limit=10)

@st.cache_data(show_spinner=False, max_entries=2)
def getCode(uri:str, color:str="black"):
    color = color.lower()
    if color != "white":
        color = "black"
    if color == "black":
        bg = "ffffff"
        target = (255, 255, 255)
    else:
        bg = "000000"
        target = (0, 0, 0)
    codeImageResponse = requests.get(f"https://spotifycodes.com/downloadCode.php?uri=png%2F{bg}%2F{color}%2F640%2F{quote(uri)}")

    finalCodeImage = convert_color_to_transparent(codeImageResponse.content, target)

    return finalCodeImage

def convert_color_to_transparent(bytes, target_color, tolerance=200):
    image = Image.open(BytesIO(bytes))
    image = image.convert("RGBA")
    pixel_data = image.getdata()
    new_pixel_data = []
    for pixel in pixel_data:
        if all(abs(pixel[i] - target_color[i]) <= tolerance for i in range(3)):
            new_pixel_data.append((pixel[0], pixel[1], pixel[2], 0))
        else:
            new_pixel_data.append(pixel)
    image.putdata(new_pixel_data)
    return image

@st.cache_data(show_spinner=False, max_entries=2)
def generateBackground(paletteName, l1style, l1shape, l1complex, l1mag, l2style, l2shape, l2complex, l2mag):
    global customPalette
    background = Canvas((700, 200))
    if paletteName != 'Custom':
        colorPaletteList = color_palettes[color_palette_names.index(paletteName)].copy()
    else:
        colorPaletteList = customPalette.copy()
    bg = choice(colorPaletteList)
    colorPaletteList.remove(bg)
    background.generate_bg(bg)
    background.generate_layer_one(l1style, l1shape, colorPaletteList, l1complex, l1mag)
    background.generate_layer_two(l2style, l2shape, colorPaletteList, l2complex, l2mag)
    return background.makeImage()

st.set_page_config(
    page_title="Fancy Spotify Codes",
    page_icon="🎶",
    layout="wide",
)

if "selectedIndex" not in st.session_state:
    st.session_state.selectedIndex = None

CARD_STYLE = {"card": {"margin":"0px", "width": "100%"}}
st.title("Fancy Spotify Codes")

mainCols = st.columns(3)

with mainCols[0]:
    st.header("1. Select a Song")
    searchQuery = st.text_input("Search a Song on Spotify")
    if searchQuery:
        with st.spinner("Fetching Songs..."):
            searchResults = searchSpotify(searchQuery)
            tracksFromResults = [i["name"] for i in searchResults["tracks"]["items"]]
            artistsFromResults = [i["artists"][0]["name"] for i in searchResults["tracks"]["items"]]
            albumCoverFromResults = [i["album"]["images"][0]["url"] for i in searchResults["tracks"]["items"]]
            resultsCols = st.columns(2)
            with resultsCols[0]:
                for i in range(0, len(tracksFromResults), 2):
                    card(tracksFromResults[i], artistsFromResults[i], albumCoverFromResults[i], styles=CARD_STYLE)
                    if st.button("Select", key=(i+5)**2, use_container_width=True):
                        selectIndex(i)
            with resultsCols[1]:
                for i in range(1, len(tracksFromResults), 2):
                    card(tracksFromResults[i], artistsFromResults[i], albumCoverFromResults[i], styles=CARD_STYLE)
                    if st.button("Select", key=(i+5)**2, use_container_width=True):
                        selectIndex(i)

with mainCols[1]:
    st.header("2. Create the Background")
    colorPalette = st.selectbox("Choose a color palette:", color_palette_names+["Custom"])
    with st.expander("Or create your own!"):
        customPaletteCols = st.columns(4)
        with customPaletteCols[0]:
            customColor1 = st.color_picker("Color 1")
        with customPaletteCols[1]:
            customColor2 = st.color_picker("Color 2")
        with customPaletteCols[2]:
            customColor3 = st.color_picker("Color 3")
        with customPaletteCols[3]:
            customColor4 = st.color_picker("Color 4")

    customPalette = [customColor1, customColor2, customColor3, customColor4]

    codeColor = st.radio("Code Color", ["White", "Black"])

    layerCols = st.columns(2)
    with layerCols[0]:
        st.subheader("Layer 1")
        layer1Style = st.selectbox("Choose a pattern for layer 1:", art_styles_list)
        layer1Shape = st.selectbox("Choose a shape for layer 1:", art_shapes_list)
        layer1Complexity = st.slider("Set the randomness for layer 1:", 10, 30)
        layer1Magnitude = [50, st.slider("Set the max shape size for layer 1:", 60, 400)]

    with layerCols[1]:
        st.subheader("Layer 2")
        layer2Style = st.selectbox("Choose a pattern for layer 2:", art_styles_list)
        layer2Shape = st.selectbox("Choose a shape for layer 2:", art_shapes_list)
        layer2Complexity = st.slider("Set the randomness for layer 2:", 10, 30)
        layer2Magnitude = [50, st.slider("Set the max shape size for layer 2:", 60, 400)]

if st.session_state.selectedIndex is not None:
    codeImage = getCode(searchResults["tracks"]["items"][st.session_state.selectedIndex]["uri"], codeColor)

    backgroundImage = generateBackground(colorPalette, layer1Style, layer1Shape, layer1Complexity, layer1Magnitude, layer2Style, layer2Shape, layer2Complexity, layer2Magnitude)

    backgroundImage.paste(codeImage, ((backgroundImage.width-codeImage.width)//2, (backgroundImage.height-codeImage.height)//2), codeImage)

with mainCols[2]:
    st.header("3. Download the Result")
    if st.session_state.selectedIndex is not None:
        st.image(backgroundImage)
        backgroundImageBytes = BytesIO()
        backgroundImage.save(backgroundImageBytes, format='PNG')
        backgroundImage_bytes = backgroundImageBytes.getvalue()
        st.download_button(
            label="Save as Image",
            data=backgroundImage_bytes,
            file_name=f"{tracksFromResults[st.session_state.selectedIndex]} Spotify Code.png",
            mime="image/png"
        )
