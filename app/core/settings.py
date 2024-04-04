from pathlib import Path
from typing import Literal

import os
from dotenv import load_dotenv
from pydantic import PositiveInt
from pydantic_settings import BaseSettings

STATIC_DIR = BASE_DIR / "static"

STATIC_DIR.mkdir(exist_ok=True)
MEDIA_DIR.mkdir(exist_ok=True)
MEDIA_DIR.mkdir(exist_ok=True)  


class LoggingSettings(BaseSettings):
    log_level: str = LogLevelTypes.INFO


class DatabaseSettings(BaseSettings):
    db_postgres_host: str
    db_postgres_host: str = os.getenv("DB_POSTGRES_HOST")
    db_postgres_port: int = 5432
    db_postgres_name: str
    db_postgres_username: str
    db_postgres_password: str
    db_postgres_name: str = os.getenv("DB_POSTGRES_NAME")
    db_postgres_username: str = os.getenv("DB_POSTGRES_USERNAME")
    db_postgres_password: str = os.getenv("DB_POSTGRES_PASSWORD")
    db_postgres_timeout: PositiveInt = 5
    db_postgres_driver: Literal["psycopg", "pycopg2"] = "psycopg"
    app_settings = Settings()