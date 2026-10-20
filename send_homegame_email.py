import os
import smtplib

from email.message import EmailMessage

# Nur senden wenn Bild existiert
if not os.path.exists("homegame_post.png"):
    print("Kein Heimspielpost vorhanden.")
    quit()

msg = EmailMessage()

msg["Subject"] = "DJK Heimspielankündigung - 1. Mannschaft"
msg["From"] = (
    f"DJK Leutershausen TT Bot "
    f"<{os.environ['EMAIL_USER']}>"
)
msg["To"] = os.environ["EMAIL_TO"]

msg.set_content(
    "Die Heimspielankündigung der 1. Mannschaft befindet sich im Anhang."
)

with open("homegame_post.png", "rb") as f:
    img_data = f.read()

msg.add_attachment(
    img_data,
    maintype="image",
    subtype="png",
    filename="homegame_post.png"
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
