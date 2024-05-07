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

code_image_response = requests.get(f"https://spotifycodes.com/downloadCode.php?uri=png%2Fffffff%2Fblack%2F640%2F{quote(results["tracks"]["items"][selected]["uri"])}")
with open(f"{results["tracks"]["items"][selected]["name"]}-{results["tracks"]["items"][selected]["artists"][0]["name"]}.png", "wb") as f:
    f.write(code_image_response.content)
new_image = convert_color_to_transparent(f"{results["tracks"]["items"][selected]["name"]}-{results["tracks"]["items"][selected]["artists"][0]["name"]}.png", (255, 255, 255), tolerance=200)
new_image = new_image.resize((new_image.width*2, new_image.height*2))
new_image = new_image.resize((new_image.width//2, new_image.height//2), resample=Image.LANCZOS)
code_file_name = f"{results["tracks"]["items"][selected]["name"]}-{results["tracks"]["items"][selected]["artists"][0]["name"]}.png"
new_image.save(code_file_name)

img_x = input("Enter the width of the image: ")
img_y = input("Enter the height of the image: ")

background = Canvas((int(img_x), int(img_y)))

cp = palette.get_random_palette()

bg = choice(cp)
cp.remove(bg)

background.generate_bg(bg)

background.generate_layer_one("Striped Horizontal", "Curves", cp, 10, [50,60])

background.generate_layer_two("Cornered", "Rings", cp, 10, [50, 51])

background.save("background")

bg_img = Image.open("background.png")
bg_img_w, bg_img_h = bg_img.size
code_image = new_image
code_image_w, code_image_h = code_image.size
bg_img.paste(code_image, ((bg_img_w - code_image_w)//2, (bg_img_h - code_image_h)//2), code_image)
bg_img.save("result.png")