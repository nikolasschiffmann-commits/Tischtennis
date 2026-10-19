from teams import TEAMS
import requests
import re
import json
from datetime import datetime, date
from zoneinfo import ZoneInfo
import os

if os.environ.get("KW"):
    KW = int(os.environ["KW"])
    JAHR = int(os.environ["JAHR"])
else:
    heute = date.today()
    KW = heute.isocalendar().week
    JAHR = heute.year

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

    if not match:
        raise Exception(
            f"__remixContext nicht gefunden: {url}"
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

adult_results_found = False

for team in ERWACHSENE:

    print(f"Lade Team: {team}")

    meetings = get_meetings(TEAMS[team])

    if meetings is None:
        raise Exception(
            f"Keine Meetings gefunden für {team}"
        )

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

                    adult_results_found = True

if not adult_results_found:

    report.append(
        "Keine Spiele in dieser Woche"
    )

report.append("")
report.append("JUGEND:")
report.append("")

youth_results_found = False

for team in JUGEND:

    print(f"Lade Team: {team}")

    meetings = get_meetings(TEAMS[team])

    if meetings is None:
        raise Exception(
            f"Keine Meetings gefunden für {team}"
        )

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

                    youth_results_found = True

if not youth_results_found:

    report.append(
        "Keine Spiele in dieser Woche"
    )

report.append("")
report.append("")
report.append("NÄCHSTE HEIMSPIELE")
report.append("")
report.append("ERWACHSENE:")
report.append("")

adult_home_found = False

for team in ERWACHSENE:

    print(f"Lade Heimspiele Team: {team}")

    meetings = get_meetings(TEAMS[team])

    if meetings is None:
        raise Exception(
            f"Keine Meetings gefunden für {team}"
        )

    home_games = []

    for day in meetings:

        date_str = list(day.keys())[0]
        games = day[date_str]

        for game in games:

            match_day = datetime.fromisoformat(
                game["date"]
            ).date()

            if (
                game["state"] == "scheduled"
                and "DJK Leutershausen" in game["team_home"]
                and match_day > kw_ende
            ):
                home_games.append(game)

    next_home = None

    if home_games:

        home_games.sort(
            key=lambda x: x["date"]
        )

        next_home = home_games[0]

    if next_home:

        adult_home_found = 
