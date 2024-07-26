import os

import boto3
# from botocore.exceptions import ClientError
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from flask.templating import render_template


def send_create_account(user):
    subject = "Confirmación de cuenta"
    name = user["name"]
    data = {
        "app_url": f"{os.getenv('FRONT_SERVER_URL')}/",
        "header": f"Hola, {name},",
        "body": "Para completar tu registro por favor ingresa al siguiente enlace.",
        "button": "Finalizar registro",
        "button_link": f"{os.getenv('FRONT_SERVER_URL')}/confirm/{user['id']}",
    }
    body = render_template("mail.html", **data)
    return send_mail(user["email"], subject, body.strip())

    # def send_mail(email, subject, body):
    #     message = email.html(
    #         html="<h1>My message</h1><strong>I've got something to tell you!</strong>",
    #         subject="A very important message",
    #         mail_from="from.email@example.com",
    #     )
    #     r = message.send(
    #         to="to.email@example.com",
    #         smtp={
    #             "host": "my-aws-smtp-server",
    #             "port": 587,
    #             "timeout": 5,
    #             "user": "my-aws-smtp-user",
    #             "password": "my-aws-smtp-pass",
    #             "tls": True,
    #         },
    #     )
    #
    #     # Check if the email was properly sent
    # assert r.status_code == 250


# def send_mail(email: str, subject: str, body: str):
#     ses_client = boto3.client("ses")

#     send_args = {
#         "Source": "noreply@traductorlsb.com",
#         "Destination": {"ToAddresses": [email]},
#         "Message": {
#             "Subject": {"Data": subject},
#             "Body": {"Html": {"Data": body}},
#         },
#     }

#     try:
#         response = ses_client.send_email(**send_args)
#         message_id = response["MessageId"]
#         print(
#             "Sent mail %s from %s to %s.",
#             message_id,
#             "noreply@traductorlsb.com",
#             email,
#         )
#     except ClientError:
#         print("Couldn't send mail from %s to %s.", "noreply@traductorlsb.com", email)
#         raise
#     else:
#         return message_id


def send_mail(email, subject, body):
    em = MIMEMultipart()
    em["From"] = str(os.getenv("EMAIL_FROM"))
    em["To"] = email
    em["Subject"] = subject
    em.attach(MIMEText(body, "html"))

    try:
        port = int(str(os.getenv("SMTP_PORT")))
        server = smtplib.SMTP(str(os.getenv("SMTP_SERVER")), port)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(str(os.getenv("SMTP_USER")), str(os.getenv("SMTP_PASSWORD")))
        server.sendmail(em["from"], email, em.as_string())
        server.close()
        return True
    except Exception as e:
        print("Error sending email", e)
        return False
