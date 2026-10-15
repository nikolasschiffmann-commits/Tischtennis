import requests
import json
import re

url = "https://www.mytischtennis.de/click-tt/ByTTV/26--27/ligen/Bezirksliga_Gruppe_1_Nordwest/gruppe/523886/mannschaft/3115893/DJK_Leutershausen/spielplan/vr"

html = requests.get(url).text

match = re.search(
    r'window\.__remixContext = ({.*?});</script>',
    html,
    re.DOTALL
)

if match:
    data = json.loads(match.group(1))
    print("JSON gefunden")
else:
    print("Kein JSON gefunden")
`
