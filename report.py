import requests
import re
import json

url = "https://www.mytischtennis.de/click-tt/ByTTV/26--27/ligen/Bezirksliga_Gruppe_1_Nordwest/gruppe/523886/mannschaft/3115893/DJK_Leutershausen/spielplan/vr"

html = requests.get(url).text

print("HTML geladen")
print(f"Länge: {len(html)} Zeichen")

# Nach eingebettetem JSON suchen
if "__remixContext" in html:
    print("RemixContext gefunden")
else:
    print("RemixContext NICHT gefunden")

match = re.search(
    r'window\.__remixContext\s*=\s*({.*?});',
    html,
    re.DOTALL
)

if match:
    print("JSON Block gefunden")
    print(match.group(1)[:1000])
else:
    print("JSON Block nicht gefunden")
