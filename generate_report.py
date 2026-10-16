import requests
import re
import json
from datetime import datetime, timedelta

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

today = datetime.today()
last_week = today - timedelta(days=7)
next_two_weeks = today + timedelta(days=14)

report = []

report.append("ERGEBNISSE LETZTE WOCHE")
report.append("")

for day in meetings:

    date_str = list(day.keys())[0]
    matches = day[date_str]

    match_date = datetime.strptime(date_str, "%Y-%m-%d")

    if last_week <= match_date <= today:

        for game in matches:

            if game["state"] == "done":

                report.append(
                    f'{game["team_home"]} - {game["team_away"]} '
                    f'{game["matches_won"]}:{game["matches_lost"]}'
                )

report.append("")
report.append("")
report.append("NÄCHSTE HEIMSPIELE")
report.append("")

for day in meetings:

    date_str = list(day.keys())[0]
    matches = day[date_str]

    match_date = datetime.strptime(date_str, "%Y-%m-%d")

    if today <= match_date <= next_two_weeks:

        for game in matches:

            if game["team_home"] == "DJK Leutershausen":

                report.append(
                    f'{date_str}: '
                    f'{game["team_home"]} - {game["team_away"]}'
                )

with open("instagram_report.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(report))

print("instagram_report.txt erstellt")
