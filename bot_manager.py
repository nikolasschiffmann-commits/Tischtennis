import json

with open(
    "teams.json",
    "r",
    encoding="utf-8"
) as f:
    teams = json.load(f)

print()
print("=== TT BOT MANAGER ===")
print()

for team, url in teams.items():
    print(f"{team}")
    print(url)
    print()
