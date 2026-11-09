import json
import tempfile
import unittest
from pathlib import Path
from datetime import date
from urllib.parse import parse_qs, urlsplit
from unittest.mock import Mock, patch

import bttv


SCHEDULE_HTML = b"""<table class='result-set'>
<tr><th>Datum</th><th>Zeit</th><th>Liga</th><th>Heimmannschaft</th><th>Gastmannschaft</th><th>Spiele</th></tr>
<tr><td>12.11.2026</td><td>19:00</td><td>BL E</td><td>DJK Leutershausen</td><td>Gegner 1</td><td>7:3</td></tr>
<tr><td></td><td>18:30</td><td>BKC E</td><td>DJK Leutershausen II</td><td>Gegner 2</td><td></td></tr>
<tr><td>13.11.2026</td><td>17:30</td><td>BKA J19</td><td>DJK Leutershausen</td><td>Gegner 3</td><td>6:4</td></tr>
<tr><td>14.11.2026</td><td>t/v</td><td>BKC J19</td><td>DJK Leutershausen II</td><td>Gegner 4</td><td></td></tr>
<tr><td>15.11.2026</td><td>18:00</td><td>BKD MJ19</td><td>DJK Leutershausen III</td><td>Gegner 5</td><td></td></tr>
<tr><td>16.11.2026</td><td>18:00</td><td>BKP E</td><td>DJK Leutershausen IV</td><td>Gegner 6</td><td></td></tr>
</table>"""


class BttvParserTests(unittest.TestCase):
    def setUp(self):
        self.original_cache_file = bttv.CACHE_FILE
        self.original_cache_loaded = bttv.CACHE_LOADED
        self.original_meetings_cache = dict(bttv.MEETINGS_CACHE)
        self.temp_dir = tempfile.TemporaryDirectory()
        bttv.CACHE_FILE = Path(self.temp_dir.name) / "cache.json"
        bttv.CACHE_LOADED = False
        bttv.MEETINGS_CACHE.clear()

    def tearDown(self):
        bttv.CACHE_FILE = self.original_cache_file
        bttv.CACHE_LOADED = self.original_cache_loaded
        bttv.MEETINGS_CACHE.clear()
        bttv.MEETINGS_CACHE.update(self.original_meetings_cache)
        self.temp_dir.cleanup()

    def test_parser_maps_all_five_teams_and_normalizes_games(self):
        with self.assertWarnsRegex(RuntimeWarning, "BKP E"):
            meetings = bttv.parse_meetings(SCHEDULE_HTML)

        self.assertEqual(set(meetings), set(bttv.TEAM_BY_LEAGUE.values()))
        for team in bttv.TEAM_BY_LEAGUE.values():
            self.assertTrue(meetings[team], f"Keine Begegnung für {team}")

        first_team_game = meetings["1. Mannschaft"][0]["2026-11-12"][0]
        self.assertEqual(first_team_game["state"], "done")
        self.assertEqual(first_team_game["matches_won"], "7")
        self.assertEqual(first_team_game["matches_lost"], "3")
        self.assertEqual(first_team_game["location"]["city"], "Leutershausen")

        second_team_game = meetings["2. Mannschaft"][0]["2026-11-12"][0]
        self.assertEqual(second_team_game["state"], "scheduled")
        self.assertTrue(second_team_game["time_available"])

        youth_two_game = meetings["Jugend II"][0]["2026-11-14"][0]
        self.assertFalse(youth_two_game["time_available"])

    def test_season_start_year_handles_july_boundary(self):
        self.assertEqual(bttv.get_season_start_year(date(2026, 6, 30)), 2025)
        self.assertEqual(bttv.get_season_start_year(date(2026, 7, 1)), 2026)

    def test_team_url_uses_configured_id_and_current_season(self):
        url = bttv.get_team_url("1. Mannschaft", date(2026, 11, 9))
        query = parse_qs(urlsplit(url).query)

        self.assertEqual(query["selectedTeamId"], [bttv.TEAM_IDS["1. Mannschaft"]])
        self.assertEqual(query["searchTimeRangeFrom"], ["01.07.2026"])
        self.assertEqual(query["searchTimeRangeTo"], ["30.06.2027"])

    def test_one_fetch_populates_and_persists_all_team_schedules(self):
        response = Mock()
        response.content = SCHEDULE_HTML
        response.raise_for_status.return_value = None

        with patch("bttv.requests.get", return_value=response) as get:
            with self.assertWarnsRegex(RuntimeWarning, "BKP E"):
                first_team = bttv.get_meetings("1. Mannschaft", 2026)
            self.assertTrue(first_team)
            get.assert_called_once()
            self.assertEqual(get.call_args.kwargs["params"]["searchTimeRangeFrom"], "01.07.2026")
            self.assertEqual(get.call_args.kwargs["params"]["searchTimeRangeTo"], "30.06.2027")

            bttv.MEETINGS_CACHE.clear()
            bttv.CACHE_LOADED = False
            second_team = bttv.get_meetings("2. Mannschaft", 2026)

        self.assertTrue(second_team)
        get.assert_called_once()
        saved_cache = json.loads(bttv.CACHE_FILE.read_text(encoding="utf-8"))
        self.assertEqual(saved_cache["version"], bttv.CACHE_VERSION)
        self.assertEqual(len(saved_cache["seasons"]["2026"]), 5)


if __name__ == "__main__":
    unittest.main()