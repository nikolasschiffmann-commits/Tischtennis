from PIL import Image, ImageDraw

img = Image.open("template.png")

draw = ImageDraw.Draw(img)

# Ergebnisse Erwachsene
draw.rectangle(
    [(140, 610), (940, 810)],
    outline="red",
    width=5
)

# Ergebnisse Jugend
draw.rectangle(
    [(140, 830), (940, 1030)],
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
