from teams import TEAMS
import requests
import re
import json
from datetime import datetime, timedelta, date

# =====================================
# HIER DIE GEWÜNSCHTE KW EINSTELLEN
# =====================================

KW = 41
JAHR = 2026

# =====================================

kw_start = date.fromisocalendar(JAHR, KW, 1)
kw_ende = date.fromisocalendar(JAHR, KW, 7)

heimspiel_ende = kw_ende + timedelta(days=30)

print(f"Auswertung KW {KW}")
print(f"Von: {kw_start}")
print(f"Bis: {kw_ende}")

report = []

report.append(f"ERGEBNISSE KW {KW}")
report.append("")

for team_name, url in TEAMS.items():

    report.append(team_name)

    html = requests.get(url).text

    match = re.search(
        r'window\.__remixContext\s*=\s*({.*?});',
        html,
        re.DOTALL
    )

    if not match:
        report.append("- Fehler beim Laden")
        report.append("")
        continue

    data = json.loads(match.group(1))

    meetings = None

    def find_meetings(obj):
        nonlocal_meetings = None

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

        match_date = datetime.strptime(
            date_str,
            "%Y-%m-%d"
        ).date()

        if kw_start <= match_date <= kw_ende:

            for game in games:

                if game["state"] == "done":

                    report.append(
                        f"- {game['team_home']} - "
                        f"{game['team_away']} "
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

    if not match:
        continue

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

        match_date = datetime.strptime(
            date_str,
            "%Y-%m-%d"
        ).date()

        if kw_ende < match_date <= heimspiel_ende:

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
``
