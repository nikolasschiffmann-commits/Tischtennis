import requests

url = "https://www.mytischtennis.de/click-tt/ByTTV/26--27/ligen/Bezirksliga_Gruppe_1_Nordwest/gruppe/523886/tabelle/vr"

html = requests.get(url).text

with open("clicktt.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Datei gespeichert")
