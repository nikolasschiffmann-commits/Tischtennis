from PIL import Image, ImageDraw

img = Image.open("template.png")

draw = ImageDraw.Draw(img)

# Ergebnisse Erwachsene
draw.rectangle(
    [(140, 620), (940, 860)],
    outline="red",
    width=5
)

# Ergebnisse Jugend
draw.rectangle(
    [(140, 880), (940, 1040)],
    outline="green",
    width=5
)

# Heimspiele Erwachsene
draw.rectangle(
    [(140, 1250), (940, 1540)],
    outline="blue",
    width=5
)

# Heimspiele Jugend
draw.rectangle(
    [(140, 1560), (940, 1850)],
    outline="yellow",
    width=5
)

img.save("instagram_post.png")

print("Bild erzeugt")
