from PIL import Image, ImageDraw

img = Image.open("template_heimspiel.png")

draw = ImageDraw.Draw(img)

# Gegnername
draw.rectangle(
    [(100, 710), (910, 880)],
    outline="red",
    width=5
)

# Spielinfos auf dem Schläger
draw.rectangle(
    [(420, 1010), (860, 1370)],
    outline="yellow",
    width=5
)

img.save("homegame_test.png")
img.show()
print("Testbild erzeugt")
