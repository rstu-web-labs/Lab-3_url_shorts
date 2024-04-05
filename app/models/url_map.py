from sqlalchemy import Integer, String, DateTime, ForeignKey, select
from sqlalchemy.orm import DeclarativeBase, mapped_column, relationship
from sqlalchemy.sql import func
from app.core.db import engine, Base, check_db_connection


class ShortUrl(Base):
    __tablename__="short_url"
    id = mapped_column(Integer, primary_key=True)
    url = mapped_column(String(2048), nullable=False, unique=True)
    short_url = mapped_column(String(150), nullable=False, unique=True)
    created_at = mapped_column(DateTime, nullable=False, default=func.now())
    
    
def create_database():
    if check_db_connection():
        Base.metadata.create_all(bind=engine)

def delete_tables():
    Base.metadata.drop_all(bind=engine)

def get_original_url(short_url, session):
    sh = 'https://tinyurl.com/' + short_url
    short_url_obj = session.execute(select(ShortUrl).filter(ShortUrl.short_url==sh)).scalars().first()
    return short_url_obj

def add_short_url(url, short_url, session):
    new_short_url = ShortUrl(url=url, short_url=short_url)
    session.add(new_short_url)
    session.commit()