import json
import re
from datetime import date, datetime
from pathlib import Path
import tempfile
from zoneinfo import ZoneInfo

import requests
from bs4 import BeautifulSoup

BTTV_MEETINGS_URL = "https://bttv.click-tt.de/cgi-bin/WebObjects/nuLigaTTDE.woa/wa/clubMeetings"
BTTV_CLUB_ID = "23774"
TEAM_BY_LEAGUE = {
    "BL E": "1. Mannschaft",
    "BKC E": "2. Mannschaft",
    "BKA J19": "Jugend I",
    "BKC J19": "Jugend II",
    "BKD MJ19": "Jugend III",
}
MEETINGS_CACHE = {}
CACHE_FILE = Path(tempfile.gettempdir()) / "tischtennis-bttv-23774-cache.json"
CACHE_LOADED = False
CACHE_VERSION = 2


def load_cached_meetings():
    global CACHE_LOADED

    if CACHE_LOADED:
        return
    CACHE_LOADED = True

    try:
        cached = json.loads(CACHE_FILE.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return

    if (
        cached.get("version") != CACHE_VERSION
        or cached.get("fetched_on") != date.today().isoformat()
    ):
        return

    for season_start_year, teams in cached.get("seasons", {}).items():
        for team, meetings in teams.items():
            MEETINGS_CACHE[(team, int(season_start_year))] = meetings


def save_cached_meetings():
    cached = {
        "version": CACHE_VERSION,
        "fetched_on": date.today().isoformat(),
        "seasons": {},
    }
    for (team, season_start_year), meetings in MEETINGS_CACHE.items():
        cached["seasons"].setdefault(str(season_start_year), {})[team] = meetings
    CACHE_FILE.write_text(
        json.dumps(cached, ensure_ascii=False),
        encoding="utf-8",
    )


def get_meetings(team, season_start_year=None):
    load_cached_meetings()

    if team not in TEAM_BY_LEAGUE.values():
        raise ValueError(f"Unbekannte Mannschaft: {team}")

    if season_start_year is None:
        today = date.today()
        season_start_year = today.year if today.month >= 7 else today.year - 1

    cache_key = (team, season_start_year)
    if cache_key in MEETINGS_CACHE:
        return MEETINGS_CACHE[cache_key]

    response = requests.get(
        BTTV_MEETINGS_URL,
        params={
            "club": BTTV_CLUB_ID,
            "searchType": "1",
            "searchTimeRangeFrom": date(season_start_year, 7, 1).strftime("%d.%m.%Y"),
            "searchTimeRangeTo": date(season_start_year + 1, 6, 30).strftime("%d.%m.%Y"),
            "selectedTeamId": "WONoSelectionString",
            "searchMeetings": "Suchen",
        },
        timeout=30,
    )
    response.raise_for_status()

    soup = BeautifulSoup(response.content, "html.parser")
    table = soup.select_one("table.result-set")
    if table is None:
        raise ValueError(f"Keine BTTV-Begegnungstabelle für {team} gefunden")

    header_row = table.select_one("tr")
    headers = [cell.get_text(" ", strip=True) for cell in header_row.select("th, td")] if header_row else []
    required_headers = ["Datum", "Zeit", "Liga", "Heimmannschaft", "Gastmannschaft", "Spiele"]
    missing_headers = [header for header in required_headers if header not in headers]
    if missing_headers:
        raise ValueError(f"Fehlende Tabellenspalten: {', '.join(missing_headers)}")

    columns = {header: headers.index(header) for header in required_headers}
    grouped_meetings = {team_name: {} for team_name in TEAM_BY_LEAGUE.values()}
    last_match_date = None

    for row in table.select("tr")[1:]:
        cells = [cell.get_text(" ", strip=True) for cell in row.select("td")]
        if len(cells) <= max(columns.values()):
            continue

        if cells[columns["Datum"]]:
            last_match_date = cells[columns["Datum"]]
        if not last_match_date:
            continue

        team_name = TEAM_BY_LEAGUE.get(cells[columns["Liga"]])
        if team_name is None:
            continue

        team_home = cells[columns["Heimmannschaft"]]
        team_away = cells[columns["Gastmannschaft"]]
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
        grouped_meetings[team_name].setdefault(match_date.isoformat(), []).append(game)

    for team_name, team_days in grouped_meetings.items():
        MEETINGS_CACHE[(team_name, season_start_year)] = [
            {match_date: games}
            for match_date, games in team_days.items()
        ]
    save_cached_meetings()
    return MEETINGS_CACHE[cache_key]