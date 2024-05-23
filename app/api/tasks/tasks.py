import smtplib
from email.message import EmailMessage
from celery import Celery
import itsdangerous
from app.config import SMTP_PASSWORD, SMTP_USER, SECRET
from app.core.settings import app_settings

SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 465
celery = Celery('tasks')
celery.conf.broker_url = app_settings.celery_broker_url
celery.conf.result_backend = app_settings.celery_result_backend

URL = "http://localhost/api/users/email-verification/"


def generate_token(email: str) -> str:
    serializer = itsdangerous.URLSafeTimedSerializer(SECRET)
    token = serializer.dumps(email, salt=SECRET)
    return token


def get_email_template(username: str, mail):
    token = generate_token(mail)
    link = f"{URL}{token}"
    email = EmailMessage()
    email['Subject'] = 'Подтверждение аккаунта'
    email['From'] = SMTP_USER
    email['To'] = mail

    email.set_content(
        '<div style="border: 3px solid black; padding: 10px">'
        f'<h1 style="color: red; text-align: center">Здравствуйте, {username}, для подтверждения регистрации на портале '
        f'Укоротитель Урлов перейдите по ссылке:</h1>'
        f'<p style="text-align: center">{link}</p>'
        '</div>',
        subtype='html'
    )
    return email


@celery.task
def send_verification_email(username: str, email: str):
    message = get_email_template(username, email)
    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.send_message(message)
