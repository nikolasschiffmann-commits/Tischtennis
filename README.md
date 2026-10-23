# Tischtennis Bot Manager

Automatisiert die Auswertung von Click-TT-Spielplänen, erzeugt Instagram- und Heimspielgrafiken und zeigt die aktuellen Informationen auf einer statischen Webseite an.

## Webseite

- `index.html` zeigt die zuletzt veröffentlichten Grafiken, das nächste Heimspiel pro Mannschaft und die Mannschaftslinks.
- `manager/index.html` stellt eine einfache Team- und Linkübersicht bereit.
- Die Links werden zentral in `teams.json` gepflegt. Die Python-Skripte laden diese Datei über `teams.py`.
- Auf der Hauptseite geänderte Links werden im lokalen Browser gespeichert. Mit „teams.json herunterladen“ erhältst du die Datei, die du anschließend im Repository ersetzen und committen musst. Die Webseite schreibt nicht selbst ins Repository.

## Automatische Abläufe

Die Workflows liegen unter `.github/workflows/` und benötigen Python 3.11 sowie `requests` und `pillow`.

### TT Agent

`check.yml` läuft sonntags um 16:00 UTC. Das entspricht 18:00 Uhr während der deutschen Sommerzeit und 17:00 Uhr während der Winterzeit. Der Workflow erstellt den Wochenbericht und `instagram_post.png`, lädt Bericht und Grafik als Actions-Artefakte hoch und committet die aktualisierte Grafik.

Bei manueller Ausführung können Kalenderwoche und Jahr angegeben werden. Eine E-Mail wird bei einem geplanten Lauf oder bei manueller Ausführung mit `send_mail: yes` verschickt.

### TT Homegame Bot

`homegame.yml` läuft täglich um 07:00 UTC (09:00 Uhr im Sommer, 08:00 Uhr im Winter). Er aktualisiert `upcoming_homegames.json` und erzeugt eine Heimspielgrafik, wenn das nächste Heimspiel der 1. Mannschaft genau zwei Tage entfernt ist. Grafik und JSON werden als Artefakte hochgeladen; die aktualisierte JSON-Datei und eine erzeugte Grafik werden ins Repository committet.

## E-Mail-Konfiguration

Für den Versand müssen folgende GitHub Actions Secrets eingerichtet sein:

- `EMAIL_USER`: Absenderadresse
- `EMAIL_PASSWORD`: App-Passwort des E-Mail-Kontos
- `EMAIL_TO`: Empfänger; mehrere Adressen mit Komma trennen

## Wichtige Dateien

- `teams.json`: Click-TT-URLs aller Mannschaften
- `generate_report.py`: Ergebnisse und nächste Heimspiele für den Wochenbericht
- `generate_upcoming_homegames.py`: nächstes Heimspiel jeder Mannschaft für die Webseite
- `generate_homegame_data.py`: Daten für die Heimspielankündigung
- `create_instagram_image.py` und `create_homegame_image.py`: PNG-Erzeugung
- `template.png` und `template_heimspiel.png`: Grafikvorlagen
- `Gagalin-Regular.otf`: Schrift für die Grafiken
