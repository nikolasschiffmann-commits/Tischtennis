from teams import TEAMS
import requests
import re
import json
from datetime import datetime, date
import os

KW = int(os.environ["KW"])
JAHR = int(os.environ["JAHR"])

kw_start = date.fromisocalendar(JAHR, KW, 1)
kw_ende = date.fromisocalendar(JAHR, KW, 7)

ERWACHSENE = ["1. Mannschaft", "2. Mannschaft"]
JUGEND = ["Jugend I", "Jugend II", "Jugend III"]


def get_meetings(url):

    html = requests.get(url).text

    match = re.search(
        r'window\.__remixContext\s*=\s*({.*?});',
        html,
        re.DOTALL
    )

    data = json.loads(match.group(1))

    meetings = None

    def find_meetings(obj):
        nonlocal meetings

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

    return meetings


report = []

report.append(f"ERGEBNISSE KW {KW}")
report.append("")
report.append("ERWACHSENE:")
report.append("")

for team in ERWACHSENE:

    meetings = get_meetings(TEAMS[team])

    for day in meetings:

        date_str = list(day.keys())[0]
        games = day[date_str]

        match_date = datetime.strptime(
            date_str,
            "%Y-%m-%d"
        ).date()

        if kw_start <= match_date <= kw_ende:

            for game in games:

                if game["state"] == "done":

                    report.append(
                        f'{game["team_home"]} - '
                        f'{game["team_away"]} '
                        f'{game["matches_won"]}:{game["matches_lost"]}'
                    )

report.append("")
report.append("JUGEND:")
report.append("")

for team in JUGEND:

    meetings = get_meetings(TEAMS[team])

    for day in meetings:

        date_str = list(day.keys())[0]
        games = day[date_str]

        match_date = datetime.strptime(
            date_str,
            "%Y-%m-%d"
        ).date()

        if kw_start <= match_date <= kw_ende:

            for game in games:

                if game["state"] == "done":

                    report.append(
                        f'{game["team_home"]} - '
                        f'{game["team_away"]} '
                        f'{game["matches_won"]}:{game["matches_lost"]}'
                    )

report.append("")
report.append("")
report.append("NÄCHSTE HEIMSPIELE")
report.append("")
report.append("ERWACHSENE:")
report.append("")

for team in ERWACHSENE:

    meetings = get_meetings(TEAMS[team])

    next_home = None

    for day in meetings:

        date_str = list(day.keys())[0]
        games = day[date_str]

        for game in games:

            if (
                game["state"] == "scheduled"
                and "DJK Leutershausen" in game["team_home"]
            ):
                next_home = game
                break

        if next_home:
            break

    if next_home:

        dt = datetime.fromisoformat(
            next_home["date"].replace("Z", "+00:00")
        )

        report.append(
            f'{next_home["team_home"]} - {next_home["team_away"]}'
        )

        report.append(
            f'AM {dt.strftime("%d.%m")} UM '
            f'{dt.strftime("%H:%M")} UHR'
        )

        report.append(
            f'{next_home["location"]["label"]}, '
            f'{next_home["location"]["city"]}'
        )

        report.append("")

report.append("JUGEND:")
report.append("")

for team in JUGEND:

    meetings = get_meetings(TEAMS[team])

    next_home = None

    for day in meetings:

        date_str = list(day.keys())[0]
        games = day[date_str]

        for game in games:

            if (
                game["state"] == "scheduled"
                and "DJK Leutershausen" in game["team_home"]
            ):
                next_home = game
                break

        if next_home:
            break

    if next_home:

        dt = datetime.fromisoformat(
            next_home["date"].replace("Z", "+00:00")
        )

        report.append(
            f'{next_home["team_home"]} - {next_home["team_away"]}'
        )

        report.append(
            f'AM {dt.strftime("%d.%m")} UM '
            f'{dt.strftime("%H:%M")} UHR'
        )

        report.append(
            f'{next_home["location"]["label"]}, '
            f'{next_home["location"]["city"]}'
        )

        report.append("")

with open(
    "instagram_report.txt",
    "w",
    encoding="utf-8"
) as f:
    f.write("\n".join(report))

print("instagram_report.txt erstellt")
