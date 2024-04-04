from sqlalchemy import Integer, String, Column, Date
from app.core.db import Base


class Post(Base):
    __tablename__ = 'urls'
    id = Column(Integer, primary_key=True)
    short_url = Column(String(100), nullable=False)
    url = Column(String(100), nullable=False)
    created_at = Column(Date, nullable=False)
