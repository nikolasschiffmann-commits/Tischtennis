import os
import smtplib
from pathlib import Path

from email.message import EmailMessage

TEAM_NAME = os.environ.get("TEAM_NAME", "1. Mannschaft")
DATA_FILE = os.environ.get("DATA_FILE", "homegame.json")
IMAGE_FILE = os.environ.get("IMAGE_FILE", "homegame_post.png")

# Nur senden wenn Bild existiert
if not os.path.exists(DATA_FILE) or not os.path.exists(IMAGE_FILE):
    print("Kein Heimspielpost vorhanden.")
    quit()

msg = EmailMessage()

msg["Subject"] = f"DJK Heimspielankündigung - {TEAM_NAME}"
msg["From"] = (
    f"DJK Leutershausen TT Bot "
    f"<{os.environ['EMAIL_USER']}>"
)
msg["To"] = os.environ["EMAIL_TO"]

msg.set_content(
    f"Die Heimspielankündigung der {TEAM_NAME} befindet sich im Anhang."
)

with open(IMAGE_FILE, "rb") as f:
    img_data = f.read()

msg.add_attachment(
    img_data,
    maintype="image",
    subtype="png",
    filename=Path(IMAGE_FILE).name
)

recipients = [
    email.strip()
    for email in os.environ["EMAIL_TO"].split(",")
]

with smtplib.SMTP_SSL(
    "smtp.gmail.com",
    465
) as smtp:

    smtp.login(
        os.environ["EMAIL_USER"],
        os.environ["EMAIL_PASSWORD"]
    )

    smtp.send_message(
        msg,
        to_addrs=recipients
    )

print("Heimspiel-Mail erfolgreich versendet")
