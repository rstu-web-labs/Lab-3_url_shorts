from sqlalchemy import Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import DeclarativeBase, mapped_column, relationship
from sqlalchemy.sql import func
from app.core.db import engine, Base, check_db_connection


class OriginalUrl(Base):
    __tablename__ = "original_short_urls"
    id = mapped_column(Integer, primary_key=True)
    url = mapped_column(String(2048), nullable=False)
    short_url = mapped_column(String(8), nullable=False, unique=True)
    created_at = mapped_column(DateTime, nullable=False, server_default=func.now())


def create_database():
    if check_db_connection():
        Base.metadata.create_all(bind=engine)


def delete_tables():
    Base.metadata.drop_all(bind=engine)
