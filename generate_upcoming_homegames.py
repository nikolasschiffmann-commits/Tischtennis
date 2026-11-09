from bttv import get_meetings
from teams import TEAMS
import json
from datetime import datetime
from zoneinfo import ZoneInfo


upcoming_homegames = []
today = datetime.now(ZoneInfo("Europe/Berlin")).date()

for team_name in TEAMS:

    print(f"Prüfe: {team_name}")

    meetings = get_meetings(team_name)

    if not meetings:
        continue

    scheduled_games = []

    for day in meetings:

        date_str = list(day.keys())[0]
        games = day[date_str]

        for game in games:

            if (
                game["state"] == "scheduled"
                and datetime.fromisoformat(game["date"]).astimezone(
                    ZoneInfo("Europe/Berlin")
                ).date() >= today
            ):
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

    upcoming_homegames.append((
        next_game["date"],
        {
            "mannschaft": team_name,
            "gegner": next_game["team_away"] if is_home else next_game["team_home"],
            "heimspiel": is_home,
            "datum": dt.strftime("%d.%m.%Y"),
            "uhrzeit": dt.strftime("%H:%M") if next_game["time_available"] else "Uhrzeit noch offen",
            "ort": next_game["location"]["city"] or "Ort nicht angegeben",
        },
    ))

upcoming_homegames.sort(key=lambda item: item[0])
upcoming_homegames = [game for _, game in upcoming_homegames]

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
