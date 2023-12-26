import os
import dotenv
import io
dotenv.load_dotenv()

from deta import Deta
from PIL import Image, ImageDraw, ImageColor

import bot.utils as utils

deta = Deta(os.getenv("DATAKEY"))
games = deta.Base("games")

def placePixels(pixels: list | tuple = ()):
    if type(pixels) == list: pixels = tuple(pixels)
    
    with open("assets/base.png", "rb") as file:
        image_bytes = file.read()
        image = Image.open(io.BytesIO(image_bytes))
    
    blank = image

    draw = ImageDraw.Draw(image)

    width, height = image.size
    slot = 40

    for pixel in pixels:
        clr = ImageColor.getrgb(pixel["color"])
        box = tuple([ int(_) for _ in pixel["place"].split("-") ])

        if 1 <= box[0] <= 26 and 1 <= box[1] <= 26:
            draw.rectangle((((box[0]) * slot, (box[1]) * slot), ((box[0]) * slot + slot, box[1] * slot + slot)), fill=clr)

    for x in range(0, width, slot):
        draw.line([(x + 40, 40), (x + 40, height)], fill = "black", width = (int(x == 0) * 2) + 4)

    for y in range(0, height, slot):
        draw.line([(40, y + 40), (width, y + 40)], fill = "black", width = (int(y == 0) * 2) + 4)

    image.save("lastmap.png")

def final(serv: int):
    current = games.get(str(serv))["pixels"]
    
    if current is None:
        placePixels()
    else:
        placePixels(current)

    utils.Game(serv).save_image(open("lastmap.png", "rb").read())