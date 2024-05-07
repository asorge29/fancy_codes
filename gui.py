import streamlit as st
from color_palettes import color_palette_names
from background_generator import art_styles_list, art_shapes_list, Canvas
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from streamlit_card import card

load_dotenv()
spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

CARD_STYLE = {"card": {"margin":"0px", "width": "100%"}}
st.title("Fancy Spotify Codes")

mainCols = st.columns(3)

with mainCols[0]:
    st.header("1. Select a Song")
    searchQuery = st.text_input("Search a Song on Spotify")
    if searchQuery:
        searchResults = spotify.search(searchQuery, type='track', limit=10)
        tracksFromResults = [i["name"] for i in searchResults["tracks"]["items"]]
        artistsFromResults = [i["artists"][0]["name"] for i in searchResults["tracks"]["items"]]
        albumCoverFromResults = [i["album"]["images"][0]["url"] for i in searchResults["tracks"]["items"]]
        resultsCols = st.columns(2)
        with resultsCols[0]:
            for i in range(0, len(tracksFromResults), 2):
                card(tracksFromResults[i], artistsFromResults[i], albumCoverFromResults[i], styles=CARD_STYLE)
        with resultsCols[1]:
            for i in range(1, len(tracksFromResults), 2):
                card(tracksFromResults[i], artistsFromResults[i], albumCoverFromResults[i], styles=CARD_STYLE)

with mainCols[1]:
    st.header("2. Create the Background")
    st.selectbox("Choose a color palette:", color_palette_names+["Custom"])
    with st.expander("Or create your own!"):
        customPaletteCols = st.columns(4)
        with customPaletteCols[0]:
            st.color_picker("Color 1")
        with customPaletteCols[1]:
            st.color_picker("Color 2")
        with customPaletteCols[2]:
            st.color_picker("Color 3")
        with customPaletteCols[3]:
            st.color_picker("Color 4")

    st.radio("Code Color", ["White", "Black"])

    layerCols = st.columns(2)
    with layerCols[0]:
        st.subheader("Layer 1")
        st.selectbox("Choose a pattern for layer 1:", art_styles_list)
        st.selectbox("Choose a shape for layer 1:", art_shapes_list)
        st.slider("Set the randomness for layer 1:", 10, 30)
        st.slider("Set the max shape size for layer 1:", 51, 400)

    with layerCols[1]:
        st.subheader("Layer 2")
        st.selectbox("Choose a pattern for layer 2:", art_styles_list)
        st.selectbox("Choose a shape for layer 2:", art_shapes_list)
        st.slider("Set the randomness for layer 2:", 10, 30)
        st.slider("Set the max shape size for layer 2:", 51, 400)

with mainCols[2]:
    st.header("3. Download the Result")