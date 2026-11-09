from bttv import get_meetings
import json
import os
from datetime import datetime
from zoneinfo import ZoneInfo

TEAM_NAME = os.environ.get("TEAM_NAME", "1. Mannschaft")
DATA_FILE = os.environ.get("DATA_FILE", "homegame.json")

meetings = get_meetings(TEAM_NAME)

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
    raise Exception(
        "Kein zukünftiges Heimspiel gefunden"
    )

home_games.sort(
    key=lambda x: x["date"]
)

next_home = home_games[0]

dt = datetime.fromisoformat(
    next_home["date"]
)

today = datetime.now(ZoneInfo("Europe/Berlin")).date()

game_date = dt.date()

days_until_game = (
    game_date - today
).days

if days_until_game != 2:
    if os.path.exists(DATA_FILE):
        os.remove(DATA_FILE)
    print(
        f"Kein Heimspiel in 2 Tagen. "
        f"Nächstes Heimspiel in {days_until_game} Tagen."
    )
    quit()

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
    "uhrzeit": (
        f"{dt.strftime('%H:%M')} UHR"
        if next_home["time_available"]
        else "UHRZEIT NOCH OFFEN"
    ),
    "ort": next_home["location"]["city"].upper()
}

with open(
    DATA_FILE,
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
print(homegame)
