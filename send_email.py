import os
import smtplib

from email.message import EmailMessage

msg = EmailMessage()

msg["Subject"] = f"DJK Instagram Post KW {KW}"
msg["From"] = os.environ["EMAIL_USER"]
msg["To"] = os.environ["EMAIL_TO"]

msg.set_content(
    "Der aktuelle Instagram-Post befindet sich im Anhang."
)

with open("instagram_post.png", "rb") as f:
    img_data = f.read()

msg.add_attachment(
    img_data,
    maintype="image",
    subtype="png",
    filename="instagram_post.png"
)

with smtplib.SMTP_SSL(
    "smtp.gmail.com",
    465
) as smtp:

    smtp.login(
        os.environ["EMAIL_USER"],
        os.environ["EMAIL_PASSWORD"]
    )

    smtp.send_message(msg)

print("E-Mail erfolgreich versendet")
