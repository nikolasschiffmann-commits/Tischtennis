from teams import TEAMS
import requests
import re
import json
from datetime import datetime, timedelta

today = datetime.today()
last_week = today - timedelta(days=7)
next_30_days = today + timedelta(days=30)

report = []

report.append("ERGEBNISSE LETZTE WOCHE")
report.append("")

for team_name, url in TEAMS.items():

    report.append(team_name)

    html = requests.get(url).text

    match = re.search(
        r'window\.__remixContext\s*=\s*({.*?});',
        html,
        re.DOTALL
    )

    data = json.loads(match.group(1))

    meetings = None

    def find_meetings(obj):
        nonlocal_meetings = False

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

    found_result = False

    for day in meetings:

        date_str = list(day.keys())[0]
        games = day[date_str]

        match_date = datetime.strptime(date_str, "%Y-%m-%d")

        if last_week <= match_date <= today:

            for game in games:

                if game["state"] == "done":

                    report.append(
                        f"- {game['team_home']} - {game['team_away']} "
                        f"{game['matches_won']}:{game['matches_lost']}"
                    )

                    found_result = True

    if not found_result:
        report.append("- Kein Spiel")

    report.append("")

report.append("")
report.append("NÄCHSTE HEIMSPIELE")
report.append("")

for team_name, url in TEAMS.items():

    html = requests.get(url).text

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
        games = day[date_str]

        match_date = datetime.strptime(date_str, "%Y-%m-%d")

        if today <= match_date <= next_30_days:

            for game in games:

                if (
                    game["state"] == "scheduled"
                    and "DJK Leutershausen" in game["team_home"]
                ):

                    report.append(
                        f"{date_str} | {team_name}"
                    )

                    report.append(
                        f"{game['team_home']} - {game['team_away']}"
                    )

                    report.append("")

with open(
    "instagram_report.txt",
    "w",
    encoding="utf-8"
) as f:
    f.write("\n".join(report))

print("instagram_report.txt erstellt")
