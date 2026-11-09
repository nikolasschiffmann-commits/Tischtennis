# Tischtennis Bot Manager

Automatisiert die Auswertung von Click-TT-Spielplänen, erzeugt Instagram- und Heimspielgrafiken und zeigt die aktuellen Informationen auf einer statischen Webseite an.

## Webseite

- `index.html` zeigt die zuletzt veröffentlichten Grafiken, das nächste Heimspiel pro Mannschaft und die Mannschaftslinks.
- `manager/index.html` stellt eine einfache Team- und Linkübersicht bereit.
- Die Links werden zentral in `teams.json` gepflegt. Die Python-Skripte laden diese Datei über `teams.py`.
- Auf der Hauptseite geänderte Links werden im lokalen Browser gespeichert. Mit „teams.json herunterladen“ erhältst du die Datei, die du anschließend im Repository ersetzen und committen musst. Die Webseite schreibt nicht selbst ins Repository.

## Automatische Abläufe

Die Workflows liegen unter `.github/workflows/` und verwenden Python 3.11 sowie die in `requirements.txt` festgelegten Paketversionen.

### TT Agent

`check.yml` läuft sonntags um 16:00 UTC. Das entspricht 18:00 Uhr während der deutschen Sommerzeit und 17:00 Uhr während der Winterzeit. Der Workflow erstellt den Wochenbericht und `instagram_post.png`, lädt Bericht und Grafik als Actions-Artefakte hoch und committet die aktualisierte Grafik.

Bei manueller Ausführung können Kalenderwoche und Jahr angegeben werden. Eine E-Mail wird bei einem geplanten Lauf oder bei manueller Ausführung mit `send_mail: yes` verschickt.

### TT Homegame Bot

`homegame.yml` läuft täglich um 07:00 UTC (09:00 Uhr im Sommer, 08:00 Uhr im Winter). Er aktualisiert `upcoming_homegames.json` und erzeugt eine Heimspielgrafik, wenn das nächste Heimspiel der 1. oder 2. Mannschaft genau zwei Tage entfernt ist. Geplante Läufe versenden E-Mails und übernehmen Änderungen automatisch. Beim manuellen Start können `send_mail` und `publish` getrennt auf `yes` oder `no` gesetzt werden; beide stehen standardmäßig auf `no`. Ohne `publish: yes` werden manuelle Ergebnisse nur als Actions-Artefakte bereitgestellt und nicht committet oder gepusht.

## E-Mail-Konfiguration

Für den Versand müssen folgende GitHub Actions Secrets eingerichtet sein:

- `EMAIL_USER`: Absenderadresse
- `EMAIL_PASSWORD`: App-Passwort des E-Mail-Kontos
- `EMAIL_TO`: Empfänger; mehrere Adressen mit Komma trennen

## Wichtige Dateien

- `teams.json`: Click-TT-URLs aller Mannschaften
- `bttv_config.json`: Vereins-ID, Saisonbeginn, Team-IDs und Zuordnung der BTTV-Liga-Kürzel
- `requirements.txt`: festgelegte Python-Abhängigkeiten
- `tests/test_bttv.py`: Offline-Tests des Spielplan-Parsers und Caches
- `team_links.js`: erstellt saisonaktuelle BTTV-Links für beide Webseiten
- `generate_report.py`: Ergebnisse und nächste Heimspiele für den Wochenbericht
- `generate_upcoming_homegames.py`: nächstes Spiel jeder Mannschaft für die Webseite
- `generate_homegame_data.py`: Daten für die Heimspielankündigungen
- `create_instagram_image.py` und `create_homegame_image.py`: PNG-Erzeugung
- `template.png`, `template_heimspiel.png` und `template_heimspiel2.png`: Grafikvorlagen
- `Gagalin-Regular.otf`: Schrift für die Grafiken

Die Parser-Tests laufen lokal mit `python -m unittest discover -s tests -v` und werden vor den Generierungsschritten in beiden Workflows ausgeführt.
