from PIL import Image, ImageDraw

img = Image.open("template.png")

draw = ImageDraw.Draw(img)

# Ergebnisse Erwachsene
draw.rectangle(
    [(120, 650), (980, 800)],
    outline="red",
    width=5
)

# Ergebnisse Jugend
draw.rectangle(
    [(120, 900), (980, 1100)],
    outline="green",
    width=5
)

# Heimspiele Erwachsene
draw.rectangle(
    [(120, 1450), (980, 1650)],
    outline="blue",
    width=5
)

# Heimspiele Jugend
draw.rectangle(
    [(120, 1750), (980, 2150)],
    outline="yellow",
    width=5
)

img.save("instagram_post.png")

print("Bild erzeugt")
