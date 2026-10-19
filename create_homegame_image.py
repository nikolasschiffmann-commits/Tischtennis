from PIL import Image, ImageDraw

img = Image.open("template_heimspiel.png")

draw = ImageDraw.Draw(img)

# Gegnername
draw.rectangle(
    [(120, 730), (960, 860)],
    outline="red",
    width=5
)

# Spielinfos auf dem Schläger
draw.rectangle(
    [(320, 1030), (760, 1370)],
    outline="yellow",
    width=5
)

img.save("homegame_test.png")
img.show()
print("Testbild erzeugt")
