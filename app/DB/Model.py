from sqlalchemy import Column, String, TIMESTAMP
from sqlalchemy.sql import func
from app.DB.Seccions import Base


class Url(Base):
    __tablename__ = "Url"

    shortUrl = Column(String, unique=True, primary_key=True)
    url = Column(String)
    created_at = Column(TIMESTAMP, default=func.now())
