from celery import Celery
import smtplib
import os
import time
from dotenv import load_dotenv
from jinja2 import Environment, FileSystemLoader
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


env = Environment(loader=FileSystemLoader("templates"))

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
def send_message_mail(recipient_email, message_content, action_message, subject_email):
    template = env.get_template("email.html")
    output = template.render(
        start_time=message_content["start_time"],
        end_time=message_content["end_time"],
        doctor_name=message_content["doctor_name"],
        place=message_content["place"],
        action_message=action_message,
    )
    to_email = recipient_email
    from_email = os.getenv("EMAIL")
    message = MIMEMultipart()
    message["Subject"] = subject_email
    message["From"] = from_email
    message["To"] = to_email

    message.attach(MIMEText(output, "html"))
    msgBody = message.as_string()
    try:
        res = server.sendmail(from_email, to_email, msgBody)
        print(res)
    except Exception as exc:
        print(exc)
