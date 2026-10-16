from PIL import Image, ImageDraw, ImageFont

img = Image.open("template.png")
draw = ImageDraw.Draw(img)

font_header = ImageFont.truetype(
    "Gagalin-Regular.otf",
    40
)

font_text = ImageFont.truetype(
    "Gagalin-Regular.otf",
    32
)

with open("instagram_report.txt", "r", encoding="utf-8") as f:
    report = f.read()

lines = [line.strip() for line in report.splitlines()]

ergebnisse_erwachsene = []
ergebnisse_jugend = []
heimspiele_erwachsene = []
heimspiele_jugend = []

section = None

for line in lines:

    if not line:
        continue

    if line.startswith("ERGEBNISSE"):
        continue

    if line == "ERWACHSENE:" and section is None:
        section = "ergebnisse_erwachsene"
        continue

    if line == "JUGEND:" and section == "ergebnisse_erwachsene":
        section = "ergebnisse_jugend"
        continue

    if line == "NÄCHSTE HEIMSPIELE":
        section = "heimspiele"
        continue

    if line == "ERWACHSENE:" and section == "heimspiele":
        section = "heimspiele_erwachsene"
        continue

    if line == "JUGEND:" and section == "heimspiele_erwachsene":
        section = "heimspiele_jugend"
        continue

    if section == "ergebnisse_erwachsene":
        ergebnisse_erwachsene.append(line)

    elif section == "ergebnisse_jugend":
        ergebnisse_jugend.append(line)

    elif section == "heimspiele_erwachsene":
        heimspiele_erwachsene.append(line)

    elif section == "heimspiele_jugend":
        heimspiele_jugend.append(line)


def draw_centered_lines(lines, start_y):

    y = start_y

    for line in lines:

        bbox = draw.textbbox(
            (0, 0),
            line,
            font=font_text
        )

        width = bbox[2] - bbox[0]

        x = (1080 - width) / 2

        draw.text(
            (x, y),
            line,
            fill=(0, 87, 110),
            font=font_text
        )

        y += 34


# Überschriften Ergebnisse

draw.text(
    (540, 630),
    "ERWACHSENE",
    anchor="mm",
    fill=(0, 87, 110),
    font=font_header
)

draw.text(
    (540, 810),
    "JUGEND",
    anchor="mm",
    fill=(0, 87, 110),
    font=font_header
)

# Überschriften Heimspiele

draw.text(
    (540, 1280),
    "ERWACHSENE",
    anchor="mm",
    fill=(0, 87, 110),
    font=font_header
)

draw.text(
    (540, 1500),
    "JUGEND",
    anchor="mm",
    fill=(0, 87, 110),
    font=font_header
)

# Inhalte

draw_centered_lines(
    ergebnisse_erwachsene,
    650
)

draw_centered_lines(
    ergebnisse_jugend,
    830
)

draw_centered_lines(
    heimspiele_erwachsene,
    1300
)

draw_centered_lines(
    heimspiele_jugend,
    1520
)

img.save("instagram_post.png")

print("Bild erzeugt")
