import requests

URL = "https://www.mytischtennis.de/click-tt/ByTTV/26--27/ligen/Bezirksliga_Gruppe_1_Nordwest/gruppe/523886/mannschaft/3115893/DJK_Leutershausen/spielplan/vr"

html = requests.get(URL).text

with open("team_page.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Seite gespeichert")
