from PIL import Image, ImageDraw

img = Image.open("template.png")

print("Bildgröße:", img.size)

draw = ImageDraw.Draw(img)

# Riesiges Testkreuz
draw.rectangle(
    [(100, 100), (800, 300)],
    fill="red"
)

draw.text(
    (150, 150),
    "TEST",
    fill="white"
)

img.save("instagram_post.png")

print("Bild erzeugt")
