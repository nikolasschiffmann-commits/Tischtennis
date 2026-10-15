import requests
import re
import json

url = "https://www.mytischtennis.de/click-tt/ByTTV/26--27/ligen/Bezirksliga_Gruppe_1_Nordwest/gruppe/523886/mannschaft/3115893/DJK_Leutershausen/spielplan/vr"

html = requests.get(url).text

match = re.search(
    r'window\.__remixContext\s*=\s*({.*?});',
    html,
    re.DOTALL
)

data = json.loads(match.group(1))

with open("remix.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("JSON exportiert")
`
