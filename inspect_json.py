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

def find_meetings(obj):
    if isinstance(obj, dict):
        for key, value in obj.items():
            if key == "meetings":
                print("\nANZAHL SPIELE:", len(value))

                print("\nERSTES SPIEL:")
                print(json.dumps(value[0], indent=2, ensure_ascii=False))

                return True

            if find_meetings(value):
                return True

    elif isinstance(obj, list):
        for item in obj:
            if find_meetings(item):
                return True

    return False

find_meetings(data)
