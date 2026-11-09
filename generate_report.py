from teams import TEAMS
import requests
import re
from bs4 import BeautifulSoup
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


BTTV_CLUB_ID = "23774"
BTTV_MEETINGS_URL = "https://bttv.click-tt.de/cgi-bin/WebObjects/nuLigaTTDE.woa/wa/clubMeetings"
MEETINGS_CACHE = {}


def get_meetings(team):

    if team in MEETINGS_CACHE:
        return MEETINGS_CACHE[team]

    team_id_match = re.search(r"/mannschaft/(\d+)/", TEAMS[team])
    if not team_id_match:
        raise ValueError(f"Keine Mannschafts-ID für {team} gefunden")

    season_start_year = kw_start.year if kw_start.month >= 7 else kw_start.year - 1
    season_start = date(season_start_year, 7, 1).strftime("%d.%m.%Y")
    season_end = date(season_start_year + 1, 6, 30).strftime("%d.%m.%Y")

    response = requests.get(
        BTTV_MEETINGS_URL,
        params={
            "club": BTTV_CLUB_ID,
            "searchType": "1",
            "searchTimeRangeFrom": season_start,
            "searchTimeRangeTo": season_end,
            "selectedTeamId": team_id_match.group(1),
            "searchMeetings": "Suchen",
        },
        timeout=30,
    )
    response.raise_for_status()

    soup = BeautifulSoup(response.content, "html.parser")
    table = soup.select_one("table.result-set")
    if table is None:
        raise ValueError(f"Keine Begegnungstabelle für {team} gefunden")

    header_row = table.select_one("tr")
    header_cells = header_row.select("th, td") if header_row else []
    headers = [cell.get_text(" ", strip=True) for cell in header_cells]
    required_headers = [
        "Datum",
        "Zeit",
        "Ort",
        "Heimmannschaft",
        "Gastmannschaft",
        "Spiele",
    ]
    missing_headers = [header for header in required_headers if header not in headers]
    if missing_headers:
        raise ValueError(f"Fehlende Tabellenspalten: {', '.join(missing_headers)}")

    columns = {header: headers.index(header) for header in required_headers}
    grouped_meetings = {}
    last_match_date = None

    for row in table.select("tr")[1:]:
        cells = [cell.get_text(" ", strip=True) for cell in row.select("td")]
        if len(cells) < len(headers):
            continue

        if cells[columns["Datum"]]:
            last_match_date = cells[columns["Datum"]]
        if not last_match_date:
            continue

        team_home = cells[headers.index("Heimmannschaft")]
        team_away = cells[headers.index("Gastmannschaft")]
        if not team_home or not team_away:
            continue

        match_date = datetime.strptime(last_match_date, "%d.%m.%Y").date()
        time_match = re.search(r"\d{1,2}:\d{2}", cells[columns["Zeit"]])
        match_time = (
            datetime.strptime(time_match.group(), "%H:%M").time()
            if time_match
            else datetime.min.time()
        )
        match_datetime = datetime.combine(
            match_date,
            match_time,
            tzinfo=ZoneInfo("Europe/Berlin"),
        )
        score_match = re.fullmatch(r"(\d+)\s*:\s*(\d+)", cells[columns["Spiele"]])
        game = {
            "date": match_datetime.isoformat(),
            "time_available": time_match is not None,
            "state": "done" if score_match else "scheduled",
            "team_home": team_home,
            "team_away": team_away,
            "matches_won": score_match.group(1) if score_match else None,
            "matches_lost": score_match.group(2) if score_match else None,
            "location": {
                "city": "Leutershausen" if "DJK Leutershausen" in team_home else None
            },
        }
        grouped_meetings.setdefault(match_date.isoformat(), []).append(game)

    meetings = [
        {match_date: games}
        for match_date, games in grouped_meetings.items()
    ]
    MEETINGS_CACHE[team] = meetings
    return meetings


report = []

report.append(f"ERGEBNISSE KW {KW}")
report.append("")
report.append("ERWACHSENE:")
report.append("")

adult_results_found = False

for team in ERWACHSENE:

    print(f"Lade Team: {team}")

    meetings = get_meetings(team)

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

    meetings = get_meetings(team)

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

    meetings = get_meetings(team)

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

        adult_home_found = True

        dt = datetime.fromisoformat(
            next_home["date"]
        ).astimezone(
            ZoneInfo("Europe/Berlin")
        )

        game_time = (
            f'UM {dt.strftime("%H:%M")} UHR'
            if next_home["time_available"]
            else "UHRZEIT NOCH OFFEN"
        )

        report.append(
            f'{next_home["team_home"]} - {next_home["team_away"]}'
        )

        report.append(
            f'AM {dt.strftime("%d.%m")} {game_time} IN '
            f'{next_home["location"]["city"].upper()}'
        )

        report.append("")

if not adult_home_found:

    report.append(
        "Aktuell keine Heimspiele geplant"
    )

report.append("")
report.append("JUGEND:")
report.append("")

youth_home_found = False

for team in JUGEND:

    print(f"Lade Heimspiele Team: {team}")

    meetings = get_meetings(team)

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

        youth_home_found = True

        dt = datetime.fromisoformat(
            next_home["date"]
        ).astimezone(
            ZoneInfo("Europe/Berlin")
        )

        game_time = (
            f'UM {dt.strftime("%H:%M")} UHR'
            if next_home["time_available"]
            else "UHRZEIT NOCH OFFEN"
        )

        report.append(
            f'{next_home["team_home"]} - {next_home["team_away"]}'
        )

        report.append(
            f'AM {dt.strftime("%d.%m")} {game_time} IN '
            f'{next_home["location"]["city"].upper()}'
        )

        report.append("")

if not youth_home_found:

    report.append(
        "Aktuell keine Heimspiele geplant"
    )

with open(
    "instagram_report.txt",
    "w",
    encoding="utf-8"
) as f:
    f.write("\n".join(report))

print("instagram_report.txt erstellt")
