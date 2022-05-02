from celery import Celery
import smtplib
import os
import time
from dotenv import load_dotenv

load_dotenv()

app = Celery("message_app", broker="redis://localhost/2")

server = smtplib.SMTP_SSL("smtp.mail.ru", 465)


@app.task
def login_app_email():
    app_email = os.getenv("EMAIL")
    email_password = os.getenv("EMAIL_PASSWORD")
    try:
        server.login(app_email, email_password)
    except Exception as exc:
        print(exc)


@app.task
def send_message_mail(recipient, message):
    app_email = os.getenv("EMAIL")
    try:
        server.sendmail(app_email, recipient, message)
    except Exception as exc:
        print(exc)
