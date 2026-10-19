from PIL import Image, ImageDraw, ImageFont

img = Image.open("template_heimspiel.png")
draw = ImageDraw.Draw(img)

font_opponent = ImageFont.truetype(
    "Gagalin-Regular.otf",
    42
)

font_info = ImageFont.truetype(
    "Gagalin-Regular.otf",
    28
)

# Gegnername
opponent = "TSV BAD KÖNIGSHOFEN"

bbox = draw.textbbox(
    (0, 0),
    opponent,
    font=font_opponent
)

text_width = bbox[2] - bbox[0]

x = (1080 - text_width) / 2

draw.text(
    (x, 760),
    opponent,
    fill="white",
    font=font_opponent
)

# Schlägertext

info_lines = [
    "FREITAG",
    "23.10.2026",
    "19:00 UHR",
    "HOHENROTH"
]

y = 1080

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

    y += 60

img.save("homegame_test.png")

print("Testbild erzeugt")
