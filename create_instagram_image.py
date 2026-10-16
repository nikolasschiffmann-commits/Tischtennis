from PIL import Image, ImageDraw, ImageFont

img = Image.open("template.png")

draw = ImageDraw.Draw(img)

# Standardschrift verwenden
font = ImageFont.truetype(
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    40
)

text = "DJK Leutershausen - Heimatverein Burglauer 10:0"

# Textbreite ermitteln
bbox = draw.textbbox(
    (0, 0),
    text,
    font=font
)

text_width = bbox[2] - bbox[0]

# Mittelpunkt des roten Kastens
x = (1080 - text_width) / 2

draw.text(
    (x, 650),
    text,
    fill=(0, 87, 110),
    font=font
)

img.save("instagram_post.png")

print("Bild erzeugt")
