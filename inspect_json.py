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

def search(obj, path=""):
    if isinstance(obj, dict):
        for key, value in obj.items():
            new_path = f"{path}.{key}" if path else key

            if key == "meetings":
                print("\nFOUND:")
                print(new_path)

            search(value, new_path)

    elif isinstance(obj, list):
        for idx, item in enumerate(obj):
            search(item, f"{path}[{idx}]")

search(data)
``
