from sqlalchemy import  Column, Integer, String, ForeignKey, MetaData
from sqlalchemy.orm import relationship
from app.core.db import Base, engine, get_session, check_db_connection

metadata = MetaData()

class Base_URL(Base):
    __tablename__ = 'Base_URL'
    id = Column(Integer, nullable=False, primary_key=True, index=True, unique=True)
    url = Column(String, nullable=False, unique=True)
    short_url = Column(String, nullable=False, unique=True)

def create_table_database():
    if check_db_connection:
        Base.metadata.create_all(bind=engine)

def delete_table_database():
    Base.metadata.drop_all(bind=engine)
