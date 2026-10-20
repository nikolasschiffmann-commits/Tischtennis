from teams import TEAMS
import requests
import re
import json
from datetime import datetime
from zoneinfo import ZoneInfo


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


upcoming_homegames = []

for team_name, url in TEAMS.items():

    print(f"Prüfe: {team_name}")

    meetings = get_meetings(url)

    if not meetings:
        continue

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

    if not home_games:
        continue

    home_games.sort(
        key=lambda x: x["date"]
    )

    next_home = home_games[0]

    dt = datetime.fromisoformat(
        next_home["date"]
    ).astimezone(
        ZoneInfo("Europe/Berlin")
    )

    upcoming_homegames.append({
        "mannschaft": team_name,
        "gegner": next_home["team_away"],
        "datum": dt.strftime("%d.%m.%Y"),
        "uhrzeit": dt.strftime("%H:%M"),
        "ort": next_home["location"]["city"]
    })

upcoming_homegames.sort(
    key=lambda x: datetime.strptime(
        x["datum"],
        "%d.%m.%Y"
    )
)

with open(
    "upcoming_homegames.json",
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        upcoming_homegames,
        f,
        ensure_ascii=False,
        indent=2
    )

print("upcoming_homegames.json erstellt")
