import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from flask.templating import render_template


def send_create_account(user):
    subject = "Confirmación de cuenta"
    name = user["name"]
    data = {
        "app_url": "https://lsb.zeroproject.dev/",
        "header": f"Hola, {name},",
        "body": "Para completar tu registro por favor ingresa al siguiente enlace.",
        "button": "Finalizar registro",
        "button_link": f"{os.getenv('FRONT_SERVER_URL')}/confirm/{user['id']}",
    }
    body = render_template("mail.html", **data)
    return send_mail(user["email"], subject, body.strip())


def send_mail(email, subject, body):
    em = MIMEMultipart()
    em["From"] = str(os.getenv("EMAIL_FROM"))
    em["To"] = email
    em["Subject"] = subject
    em.attach(MIMEText(body, "html"))

    try:
        port = int(str(os.getenv("SMTP_PORT")))
        with smtplib.SMTP(str(os.getenv("SMTP_SERVER")), port) as smtp:
            smtp.login(str(os.getenv("SMTP_USER")), str(os.getenv("SMTP_PASSWORD")))
            smtp.sendmail(em["from"], email, em.as_string())
        return True
    except Exception as e:
        print(e)
        return False
