from sqlalchemy import Column, String, DateTime
from app.core.db import Base
from sqlalchemy.sql import func

class UrlMap(Base):
    __tablename__ = 'url_map'
    short_url = Column(String, primary_key=True)
    original_url = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())