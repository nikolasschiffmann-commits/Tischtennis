import json

with open(
    "teams.json",
    "r",
    encoding="utf-8"
) as f:
    TEAMS = json.load(f)
