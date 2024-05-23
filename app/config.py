import os
from dotenv import load_dotenv

load_dotenv()

SMTP_USER = os.environ.get("SMTP_USER")
SMTP_PASSWORD = os.environ.get("SMTP_PASSWORD")
SECRET = os.environ.get("SMTP_PASSWORD")

REDIS_HOST = os.environ.get("REDIS_HOST")
