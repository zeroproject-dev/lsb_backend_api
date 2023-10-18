import os
import smtplib
from email.message import EmailMessage

from flask.templating import render_template


def send_create_account(user):
    subject = "Confirmación de cuenta"
    name = user['name']
    data = {
        'app_url': 'https://lsb.zeroproject.dev/',
        'header': f'Hola, {name},',
        'body': 'Para completar tu registro por favor ingresa al siguiente enlace.',
        'button': 'Finalizar registro',
        'button_link': 'https://lsb.zeroproject.dev'
    }
    body = render_template('mail.html', **data)
    return send_mail(user['email'], subject, body.strip())


def send_mail(email, subject, body):
    em = EmailMessage()
    em['From'] = str(os.getenv('EMAIL_FROM'))
    em['To'] = email
    em['Subject'] = subject
    em.set_content(body)

    try:
        port = int(str(os.getenv('SMTP_PORT')))
        with smtplib.SMTP(str(os.getenv('SMTP_SERVER')), port) as smtp:
            smtp.login(str(os.getenv('SMTP_USER')),
                       str(os.getenv('SMTP_PASSWORD')))
            smtp.sendmail(em['from'], email, em.as_string())
        return True
    except Exception as e:
        print(e)
        return False
