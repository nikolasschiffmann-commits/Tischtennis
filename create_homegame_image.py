from PIL import Image, ImageDraw, ImageFont

img = Image.open("template_heimspiel.png")
draw = ImageDraw.Draw(img)

font_opponent = ImageFont.truetype(
    "Gagalin-Regular.otf",
    50
)

font_info = ImageFont.truetype(
    "Gagalin-Regular.otf",
    34
)

# Gegnername
opponent_lines = [
    "VS",
    "TSV BAD KÖNIGSHOFEN"
]

y = 730

for line in opponent_lines:

    bbox = draw.textbbox(
        (0, 0),
        line,
        font=font_opponent
    )

    width = bbox[2] - bbox[0]

    x = 540 - width / 2

    draw.text(
        (x, y),
        line,
        fill="white",
        font=font_opponent
    )

    y += 75

# Schlägertext

info_lines = [
    "FREITAG",
    "23.10.2026",
    "19:00 UHR",
    "HOHENROTH"
]

y = 1110

for line in info_lines:

    bbox = draw.textbbox(
        (0, 0),
        line,
        font=font_info
    )

    width = bbox[2] - bbox[0]

    x = 540 - width / 2

    draw.text(
        (x, y),
        line,
        fill="white",
        font=font_info
    )

    y += 70

img.save("homegame_test.png")

print("Testbild erzeugt")
