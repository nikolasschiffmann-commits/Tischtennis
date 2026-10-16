from PIL import Image, ImageDraw

img = Image.open("template.png")

draw = ImageDraw.Draw(img)

# Ergebnisse Erwachsene
draw.text(
    (160, 630),
    "DJK Leutershausen - Heimatverein Burglauer 10:0",
    fill="black"
)

# Ergebnisse Jugend
draw.text(
    (160, 820),
    "DJK Leutershausen II - TSV Arnshausen II 8:2\n"
    "DJK Leutershausen III - Heimatverein Burglauer IV 6:4",
    fill="black"
)

# Heimspiele Erwachsene
draw.text(
    (160, 1270),
    "DJK Leutershausen - DJK Brebersdorf\n"
    "AM 16.10 UM 19:00 UHR IN HOHENROTH",
    fill="black"
)

# Heimspiele Jugend
draw.text(
    (160, 1530),
    "DJK Leutershausen II - TSV Bad Königshofen V\n"
    "AM 22.10 UM 17:30 UHR IN LEUTERSHAUSEN",
    fill="black"
)

img.save("instagram_post.png")

print("Bild erzeugt")
