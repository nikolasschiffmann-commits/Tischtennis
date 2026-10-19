from teams import TEAMS
import requests
import re
import json

URL = TEAMS["1. Mannschaft"]


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


meetings = get_meetings(URL)

home_games = []

for day in meetings:

    date_str = list(day.keys())[0]
    games = day[date_str]

    for game in games:

        if (
            game["state"] == "scheduled"
            and "DJK Leutershausen" in game["team_home"]
        ):
            home_games.append(game)

home_games.sort(
    key=lambda x: x["date"]
)

next_home = home_games[0]

dt = datetime.fromisoformat(
    next_home["date"]
)

wochentage = {
    "Monday": "MONTAG",
    "Tuesday": "DIENSTAG",
    "Wednesday": "MITTWOCH",
    "Thursday": "DONNERSTAG",
    "Friday": "FREITAG",
    "Saturday": "SAMSTAG",
    "Sunday": "SONNTAG"
}

homegame = {
    "gegner": next_home["team_away"],
    "wochentag": wochentage[dt.strftime("%A")],
    "datum": dt.strftime("%d.%m.%Y"),
    "uhrzeit": dt.strftime("%H:%M UHR"),
    "ort": next_home["location"]["city"].upper()
}

with open(
    "homegame.json",
    "w",
    encoding="utf-8"
) as f:
    json.dump(
        homegame,
        f,
        ensure_ascii=False,
        indent=2
    )

print("homegame.json erstellt")
