import requests
import re
import json

URL = "https://www.mytischtennis.de/click-tt/ByTTV/26--27/ligen/Bezirksliga_Gruppe_1_Nordwest/gruppe/523886/mannschaft/3115893/DJK_Leutershausen/spielplan/vr"

html = requests.get(URL).text

match = re.search(
    r'window\.__remixContext\s*=\s*({.*?});',
    html,
    re.DOTALL
)

data = json.loads(match.group(1))

meetings = None

def find_meetings(obj):
    global meetings

    if meetings:
        return

    if isinstance(obj, dict):
        for key, value in obj.items():

            if key == "meetings":
                meetings = value
                return

            find_meetings(value)

    elif isinstance(obj, list):
        for item in obj:
            find_meetings(item)

find_meetings(data)

for day in meetings:

    date_str = list(day.keys())[0]
    matches = day[date_str]

    print("\n-----")
    print(date_str)

    for game in matches:

        print("HOME:", game["team_home"])
        print("AWAY:", game["team_away"])
        print("STATE:", game["state"])
        print("RESULT:", game["matches_won"], ":", game["matches_lost"])
