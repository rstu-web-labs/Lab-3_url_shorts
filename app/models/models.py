from fastapi_users.db import SQLAlchemyBaseUserTable
from sqlalchemy import Column, String, DateTime, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.sql import func
from app.core.db import Base


class UrlMap(Base):
    __tablename__ = 'url_map'
    short_url = Column(String, primary_key=True)
    original_url = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    counter = Column(Integer, default=0)
    user = Column(Integer, ForeignKey("user.id"), nullable=True)
    __table_args__ = (UniqueConstraint("user", "short_url"),)


class User(SQLAlchemyBaseUserTable[int], Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False, unique=True)
    username = Column(String, nullable=False)
    registered_at = Column(DateTime(timezone=True), server_default=func.now())
