import json
from PIL import Image, ImageDraw, ImageFont

img = Image.open("template_heimspiel.png")
draw = ImageDraw.Draw(img)

with open(
    "homegame.json",
    "r",
    encoding="utf-8"
) as f:
    homegame = json.load(f)

font_opponent = ImageFont.truetype(
    "Gagalin-Regular.otf",
    75
)

font_info = ImageFont.truetype(
    "Gagalin-Regular.otf",
    75
)

# Gegnername

opponent_lines = [
    "VS",
    homegame["gegner"].upper()
]

y = 680

for line in opponent_lines:

    bbox = draw.textbbox(
        (0, 0),
        line,
        font=font_opponent
    )

    width = bbox[2] - bbox[0]

    x = 520 - width / 2

    draw.text(
        (x, y),
        line,
        fill="white",
        font=font_opponent
    )

    y += 85

# Schlägertext

info_lines = [
    homegame["wochentag"],
    homegame["datum"],
    homegame["uhrzeit"],
    homegame["ort"]
]

y = 990

for line in info_lines:

    bbox = draw.textbbox(
        (0, 0),
        line,
        font=font_info
    )

    width = bbox[2] - bbox[0]

    x = 640 - width / 2

    draw.text(
        (x, y),
        line,
        fill="white",
        font=font_info
    )

    y += 85

img.save("homegame_test.png")

print("homegame_test.png erstellt")
