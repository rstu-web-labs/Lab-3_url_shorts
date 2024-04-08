import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from typing import Literal

DB_USER = os.getenv("db_postgres_username")
DB_PASSWORD = os.getenv("db_postgres_password")
DB_HOST = os.getenv("db_postgres_host")
DB_NAME = os.getenv("db_postgres_name")
DB_DRIVER: Literal["psycopg", "pycopg2"] = "psycopg"
DB_POSTGRES_PORT = os.getenv("db_postgres_port")
engine = create_engine(
    f"postgresql+{DB_DRIVER}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_POSTGRES_PORT}/{DB_NAME}"
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()