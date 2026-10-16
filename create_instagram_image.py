from PIL import Image, ImageDraw

img = Image.open("template.png")

draw = ImageDraw.Draw(img)

# Ergebnisse Erwachsene
draw.rectangle(
    [(140, 640), (940, 820)],
    outline="red",
    width=5
)

# Ergebnisse Jugend
draw.rectangle(
    [(140, 880), (940, 1090)],
    outline="green",
    width=5
)

# Heimspiele Erwachsene
draw.rectangle(
    [(140, 1450), (940, 1640)],
    outline="blue",
    width=5
)

# Heimspiele Jugend
draw.rectangle(
    [(140, 1720), (940, 2130)],
    outline="yellow",
    width=5
)

img.save("instagram_post.png")

print("Bild erzeugt")
