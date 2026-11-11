import json
import re
import warnings
from datetime import date, datetime, timedelta
from pathlib import Path
import tempfile
from urllib.parse import parse_qs, urlencode, urlsplit, urlunsplit
from zoneinfo import ZoneInfo

import requests
from bs4 import BeautifulSoup
from teams import TEAMS

CONFIG_PATH = Path(__file__).with_name("bttv_config.json")
BTTV_CONFIG = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
BTTV_MEETINGS_URL = "https://bttv.click-tt.de/cgi-bin/WebObjects/nuLigaTTDE.woa/wa/clubMeetings"
BTTV_CLUB_ID = str(BTTV_CONFIG["club_id"])
SEASON_START_MONTH = int(BTTV_CONFIG["season_start_month"])
TEAM_IDS = BTTV_CONFIG["team_ids"]
TEAM_BY_LEAGUE = BTTV_CONFIG["teams_by_league"]
if (
    not isinstance(TEAM_BY_LEAGUE, dict)
    or len(TEAM_BY_LEAGUE) != len(TEAMS)
    or set(TEAM_BY_LEAGUE.values()) != set(TEAMS)
    or not isinstance(TEAM_IDS, dict)
    or len(TEAM_IDS) != len(TEAMS)
    or set(TEAM_IDS) != set(TEAMS)
    or len(set(TEAM_IDS.values())) != len(TEAMS)
):
    raise ValueError("BTTV-Teamzuordnung und IDs müssen alle Teams aus teams.json eindeutig enthalten")
if not 1 <= SEASON_START_MONTH <= 12:
    raise ValueError("season_start_month muss zwischen 1 und 12 liegen")

MEETINGS_CACHE = {}
CACHE_FILE = Path(tempfile.gettempdir()) / f"tischtennis-bttv-{BTTV_CLUB_ID}-cache.json"
CACHE_LOADED = False
CACHE_VERSION = 5
CACHE_CONFIG_SIGNATURE = json.dumps(BTTV_CONFIG, ensure_ascii=False, sort_keys=True)


def load_cached_meetings():
    global CACHE_LOADED

    if CACHE_LOADED:
        return
    CACHE_LOADED = True

    try:
        cached = json.loads(CACHE_FILE.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return

    if not isinstance(cached, dict):
        return

    if (
        cached.get("version") != CACHE_VERSION
        or cached.get("fetched_on") != date.today().isoformat()
        or cached.get("config_signature") != CACHE_CONFIG_SIGNATURE
        or not isinstance(cached.get("seasons"), dict)
    ):
        return

    for season_start_year, teams in cached.get("seasons", {}).items():
        for team, meetings in teams.items():
            MEETINGS_CACHE[(team, int(season_start_year))] = meetings


def save_cached_meetings():
    cached = {
        "version": CACHE_VERSION,
        "fetched_on": date.today().isoformat(),
        "config_signature": CACHE_CONFIG_SIGNATURE,
        "seasons": {},
    }
    for (team, season_start_year), meetings in MEETINGS_CACHE.items():
        cached["seasons"].setdefault(str(season_start_year), {})[team] = meetings
    CACHE_FILE.write_text(
        json.dumps(cached, ensure_ascii=False),
        encoding="utf-8",
    )


def get_season_start_year(reference_date=None):
    reference_date = reference_date or date.today()
    return (
        reference_date.year
        if reference_date.month >= SEASON_START_MONTH
        else reference_date.year - 1
    )


def get_team_url(team, reference_date=None):
    if team not in TEAM_IDS:
        raise ValueError(f"Unbekannte Mannschaft: {team}")

    season_start_year = get_season_start_year(reference_date)
    season_start = date(season_start_year, SEASON_START_MONTH, 1)
    season_end = date(season_start_year + 1, SEASON_START_MONTH, 1) - timedelta(days=1)
    parsed_url = urlsplit(TEAMS[team])
    query = parse_qs(parsed_url.query)
    query.update({
        "club": [BTTV_CLUB_ID],
        "searchType": ["1"],
        "searchTimeRangeFrom": [season_start.strftime("%d.%m.%Y")],
        "searchTimeRangeTo": [season_end.strftime("%d.%m.%Y")],
        "selectedTeamId": [TEAM_IDS[team]],
        "searchMeetings": ["Suchen"],
    })
    return urlunsplit(parsed_url._replace(query=urlencode(query, doseq=True)))


def parse_meetings(content):
    soup = BeautifulSoup(content, "html.parser")
    table = soup.select_one("table.result-set")
    if table is None:
        raise ValueError("Keine BTTV-Begegnungstabelle gefunden")

    header_row = table.select_one("tr")
    headers = [cell.get_text(" ", strip=True) for cell in header_row.select("th, td")] if header_row else []
    required_headers = ["Datum", "Zeit", "Liga", "Heimmannschaft", "Gastmannschaft", "Spiele", "Ort"]
    missing_headers = [header for header in required_headers if header not in headers]
    if missing_headers:
        raise ValueError(f"Fehlende Tabellenspalten: {', '.join(missing_headers)}")

    columns = {header: headers.index(header) for header in required_headers}
    grouped_meetings = {team_name: {} for team_name in TEAM_BY_LEAGUE.values()}
    last_match_date = None
    unknown_leagues = set()

    for row in table.select("tr")[1:]:
        cells = [cell.get_text(" ", strip=True) for cell in row.select("td")]
        if len(cells) <= max(columns.values()):
            continue

        if cells[columns["Datum"]]:
            last_match_date = cells[columns["Datum"]]
        if not last_match_date:
            continue

        team_home = cells[columns["Heimmannschaft"]]
        team_away = cells[columns["Gastmannschaft"]]
        venue_number = cells[columns["Ort"]]
        if not team_home or not team_away:
            continue

        league_code = cells[columns["Liga"]]
        team_name = TEAM_BY_LEAGUE.get(league_code)
        if team_name is None:
            if "DJK Leutershausen" in team_home or "DJK Leutershausen" in team_away:
                unknown_leagues.add(league_code)
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
                "city": (
                    {"1": "Leutershausen", "2": "Hohenroth"}.get(venue_number)
                    if "DJK Leutershausen" in team_home
                    else None
                )
            },
        }
        grouped_meetings[team_name].setdefault(match_date.isoformat(), []).append(game)

    if unknown_leagues:
        warnings.warn(
            "Unbekannte BTTV-Liga-Kürzel für DJK Leutershausen: "
            + ", ".join(sorted(unknown_leagues)),
            RuntimeWarning,
            stacklevel=2,
        )

    return {
        team_name: [
            {match_date: games}
            for match_date, games in team_days.items()
        ]
        for team_name, team_days in grouped_meetings.items()
    }


def get_meetings(team, season_start_year=None):
    load_cached_meetings()

    if team not in TEAM_BY_LEAGUE.values():
        raise ValueError(f"Unbekannte Mannschaft: {team}")

    if season_start_year is None:
        season_start_year = get_season_start_year()

    cache_key = (team, season_start_year)
    if cache_key in MEETINGS_CACHE:
        return MEETINGS_CACHE[cache_key]

    season_start = date(season_start_year, SEASON_START_MONTH, 1)
    next_season_start = date(season_start_year + 1, SEASON_START_MONTH, 1)
    season_end = next_season_start - timedelta(days=1)
    response = requests.get(
        BTTV_MEETINGS_URL,
        params={
            "club": BTTV_CLUB_ID,
            "searchType": "1",
            "searchTimeRangeFrom": season_start.strftime("%d.%m.%Y"),
            "searchTimeRangeTo": season_end.strftime("%d.%m.%Y"),
            "selectedTeamId": "WONoSelectionString",
            "searchMeetings": "Suchen",
        },
        timeout=30,
    )
    response.raise_for_status()

    meetings_by_team = parse_meetings(response.content)
    for team_name in TEAM_BY_LEAGUE.values():
        MEETINGS_CACHE[(team_name, season_start_year)] = meetings_by_team[team_name]
    save_cached_meetings()
    return MEETINGS_CACHE[cache_key]