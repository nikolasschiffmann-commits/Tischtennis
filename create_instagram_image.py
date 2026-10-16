from PIL import Image, ImageDraw
 
img = Image.open("template.png")
 
draw = ImageDraw.Draw(img)
 
draw.text(
(200, 500),
"TEST",
fill="black"
)
 
img.save("instagram_post.png")
 
print("Bild erzeugt")
