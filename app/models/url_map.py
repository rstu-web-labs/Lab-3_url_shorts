from sqlalchemy import Integer, String, Column, Date
from app.core.db import Base

class url_table(Base):
    __tablename__ = 'URL'
    id = Column(Integer, primary_key=True)
    short_url = Column(String(100), nullable=False)
    origin_url = Column(String(100), nullable=False)
    created_at = Column(String(100), nullable=False)