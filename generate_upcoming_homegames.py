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

    scheduled_games = []

    for day in meetings:

        date_str = list(day.keys())[0]
        games = day[date_str]

        for game in games:

            if game["state"] == "scheduled":
                scheduled_games.append(game)

    if not scheduled_games:
        continue

    next_game = min(
        scheduled_games,
        key=lambda game: game["date"]
    )

    is_home = "DJK Leutershausen" in next_game["team_home"]
    dt = datetime.fromisoformat(
        next_game["date"]
    ).astimezone(
        ZoneInfo("Europe/Berlin")
    )

    upcoming_homegames.append({
        "mannschaft": team_name,
        "gegner": next_game["team_away"] if is_home else next_game["team_home"],
        "heimspiel": is_home,
        "datum": dt.strftime("%d.%m.%Y"),
        "uhrzeit": dt.strftime("%H:%M"),
        "ort": next_game["location"]["city"]
    })

upcoming_homegames.sort(
    key=lambda game: datetime.strptime(
        f'{game["datum"]} {game["uhrzeit"]}',
        "%d.%m.%Y %H:%M"
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
