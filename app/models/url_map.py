from sqlalchemy import Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import DeclarativeBase, mapped_column, relationship
from sqlalchemy.sql import func
from app.core.db import engine, Base, check_db_connection

class OriginalUrl(Base):
    __tablename__ = "original_url"
    id = mapped_column(Integer, primary_key=True)
    url = mapped_column(String(2048), nullable=False, unique=True)
    
    short_urls = relationship("ShortUrl", back_populates="urls")

class ShortUrl(Base):
    __tablename__="short_url"
    id = mapped_column(Integer, primary_key=True)
    url_id = mapped_column(Integer,ForeignKey("original_url.id", ondelete="CASCADE"))
    short_url = mapped_column(String(8), nullable=False, unique=True)
    created_at = mapped_column(DateTime, nullable=False, default=func.now())
    
    urls = relationship("OriginalUrl", back_populates="short_urls")
    
    
def create_database():
    if check_db_connection():
        Base.metadata.create_all(bind=engine)

def delete_tables():
    Base.metadata.drop_all(bind=engine)
