import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import json
from urllib.parse import quote
import requests
from PIL import Image
from dotenv import load_dotenv
from random import choice, randint

from background_generator import Canvas
from color_palettes import Palette

palette = Palette()

def convert_color_to_transparent(image_path, target_color, tolerance=200):
    image = Image.open(image_path)

    image = image.convert('RGBA')

    pixel_data = image.getdata()

    new_pixel_data = []
    for pixel in pixel_data:
        if all(abs(pixel[i] - target_color[i]) <= tolerance for i in range(3)):
            new_pixel_data.append((pixel[0], pixel[1], pixel[2], 0))
        else:
            new_pixel_data.append(pixel)

    image.putdata(new_pixel_data)

    return image

load_dotenv()

spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

search = input("Search: ")
results = spotify.search(search, type="track", limit=10)
with open("results.json", 'w') as f:
    f.write(str(json.dumps(results["tracks"]["items"], indent=2)))

for i in range(len(results["tracks"]["items"])):
    print(f"{i+1}. {results["tracks"]["items"][i]["name"]} by {results["tracks"]["items"][i]["artists"][0]["name"]}")

selected = int(input("Choose a song: ")) - 1

code_image = requests.get(f"https://spotifycodes.com/downloadCode.php?uri=png%2F000000%2Fwhite%2F640%2F{quote(results["tracks"]["items"][selected]["uri"])}")
with open(f"{results["tracks"]["items"][i]["name"]}-{results["tracks"]["items"][selected]["artists"][0]["name"]}.png", "wb") as f:
    f.write(code_image.content)
new_image = convert_color_to_transparent(f"{results["tracks"]["items"][selected]["name"]}-{results["tracks"]["items"][selected]["artists"][0]["name"]}.png", (0, 0, 0), tolerance=200)
new_image.save(f"{results["tracks"]["items"][selected]["name"]}-{results["tracks"]["items"][selected]["artists"][0]["name"]}.png")

img_x = input("Enter the width of the image: ")
img_y = input("Enter the height of the image: ")

background = Canvas((int(img_x), int(img_y)))

cp = palette.get_random_palette()

bg = choice(cp)
cp.remove(bg)

background.generate_bg(bg)

background.generate_layer_one("Mosaic", "Circles", cp, randint(10, 31), randint(50, 401))

background.generate_layer_two("Cornered", "Rings", cp, randint(10, 31), randint(50, 401))

background.save("background")