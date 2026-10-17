import os
import smtplib

from datetime import date
from email.message import EmailMessage

# KW bestimmen
if os.environ.get("KW"):
    kw = os.environ["KW"]
else:
    kw = str(date.today().isocalendar().week)

msg = EmailMessage()

msg["Subject"] = f"DJK Instagram Post KW {kw}"
msg["From"] = os.environ["EMAIL_USER"]
msg["To"] = os.environ["EMAIL_TO"]

msg.set_content(
    f"Der automatisch erzeugte Instagram-Post für KW {kw} befindet sich im Anhang."
)

with open("instagram_post.png", "rb") as f:
    img_data = f.read()

msg.add_attachment(
    img_data,
    maintype="image",
    subtype="png",
    filename=f"instagram_post_KW{kw}.png"
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

print(f"E-Mail für KW {kw} erfolgreich versendet")
