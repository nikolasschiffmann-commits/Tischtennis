from PIL import Image, ImageDraw, ImageFont

img = Image.open("template.png")
draw = ImageDraw.Draw(img)

font = ImageFont.truetype(
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    26
)

with open("instagram_report.txt", "r", encoding="utf-8") as f:
    report = f.read()

lines = report.splitlines()

erw_results = []
jug_results = []
erw_home = []
jug_home = []

section = None

for line in lines:

    line = line.strip()

    if line == "ERWACHSENE:" and section is None:
        section = "erw_results"
        continue

    if line == "JUGEND:" and section == "erw_results":
        section = "jug_results"
        continue

    if line == "NÄCHSTE HEIMSPIELE":
        section = None
        continue

    if line == "ERWACHSENE:" and section is None:
        section = "erw_home"
        continue

    if line == "JUGEND:" and section == "erw_home":
        section = "jug_home"
        continue

    if not line:
        continue

    if line.startswith("ERGEBNISSE"):
        continue

    if section == "erw_results":
        erw_results.append(line)

    elif section == "jug_results":
        jug_results.append(line)

    elif section == "erw_home":
        erw_home.append(line)

    elif section == "jug_home":
        jug_home.append(line)


def draw_centered_block(text_lines, center_x, start_y):

    y = start_y

    for line in text_lines:

        bbox = draw.textbbox(
            (0, 0),
            line,
            font=font
        )

        width = bbox[2] - bbox[0]

        x = center_x - width / 2

        draw.text(
            (x, y),
            line,
            fill=(0, 87, 110),
            font=font
        )

        y += 38


draw_centered_block(
    erw_results,
    540,
    630
)

draw_centered_block(
    jug_results,
    540,
    820
)

draw_centered_block(
    erw_home,
    540,
    1270
)

draw_centered_block(
    jug_home,
    540,
    1530
)

img.save("instagram_post.png")

print("Bild erzeugt")
