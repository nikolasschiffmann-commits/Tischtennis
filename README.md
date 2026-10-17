DJK Leutershausen Instagram Bot
Zweck
Dieses Projekt erstellt automatisch den wöchentlichen Instagram-Post der Tischtennis-Abteilung der DJK Leutershausen.

Jeden Sonntag werden die Ergebnisse der aktuellen Kalenderwoche sowie die nächsten Heimspiele aus Click-TT ausgelesen, grafisch aufbereitet und per E-Mail versendet.

Funktionen
Auswertung von Click-TT / myTischtennis
Ergebnisse einer frei wählbaren Kalenderwoche
Ermittlung des nächsten Heimspiels jeder Mannschaft
Automatische Erstellung einer Instagram-Grafik
Automatischer Mailversand
Manuelle und automatische Ausführung über GitHub Actions
Ausgewertete Mannschaften
Erwachsene
Mannschaft
Mannschaft
Jugend
Jugend I
Jugend II
Jugend III
Die Mannschaften und zugehörigen Click-TT-Links werden in teams.py gepflegt.

Projektdateien
teams.py
generate_report.py
create_instagram_image.py
send_email.py
template.png
Gagalin.otf
instagram_report.txt
.github/workflows/check.yml
teams.py
Enthält die Click-TT Spielplan-URLs aller Mannschaften.

generate_report.py
Liest Click-TT aus
Ermittelt Ergebnisse der gewählten KW
Ermittelt die nächsten Heimspiele
Erstellt instagram_report.txt
create_instagram_image.py
Liest instagram_report.txt
Befüllt das Instagram-Template
Erstellt instagram_post.png
send_email.py
Versendet die fertige Grafik per E-Mail
Betreff enthält automatisch die Kalenderwoche
GitHub Secrets
Folgende Secrets müssen eingerichtet sein:

EMAIL_USER
Bot-Mailadresse

Beispiel:

djk.tt.instagram@gmail.com
EMAIL_PASSWORD
Google App-Passwort

Nicht das normale Gmail-Passwort verwenden.

EMAIL_TO
Empfängerliste.

Mehrere Empfänger werden durch Komma getrennt:

adresse1@gmail.com,adresse2@gmail.com
Workflow
Datei:

.github/workflows/check.yml
Manuelle Ausführung
Actions
→ TT Agent
→ Run workflow
Parameter:

KW
Jahr
Automatische Ausführung
Jeden Sonntag um 18:00 Uhr.

Cron:

schedule:
  - cron: '0 16 * * 0'
Ablauf
GitHub Action

↓

Click-TT auslesen

↓

Report erzeugen

↓

Instagram-Grafik erzeugen

↓

E-Mail versenden

↓

Fertiger Instagram-Post
Layoutbereiche
Ergebnisse Erwachsene
X: 140 - 940
Y: 610 - 790
Ergebnisse Jugend
X: 140 - 940
Y: 800 - 1030
Heimspiele Erwachsene
X: 140 - 940
Y: 1250 - 1500
Heimspiele Jugend
X: 140 - 940
Y: 1510 - 1850
Verwendete Schrift
Gagalin.otf
Wartung
Neue Empfänger hinzufügen
Settings
→ Secrets and Variables
→ Actions
→ EMAIL_TO
Mehrere Empfänger mit Komma trennen.

Mannschaften ändern
Datei:

teams.py
anpassen.

Instagram-Layout ändern
Datei:

create_instagram_image.py
anpassen.

Versionsstand
Aktueller produktiver Stand:

v1.0
