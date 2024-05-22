import sqlalchemy
from app.core.db import Base, engine
from app.models.url_map import Base_URL
from sqlalchemy.orm import Session
from app.models.url_map import Base_URL
from app.models.schema import  Forma_Base_URL, Forma_Short_URL
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import select, insert
from typing import List

def set_original_url(db: Session, data: Base_URL) -> bool:
    stmt = insert(Base_URL).values(url=str(data.url), short_url=str(data.short_url))
    db.execute(stmt)
    db.commit()
    return True


def get_short_url_in(db: Session, short_url: str):
    stmt = select(Base_URL).where(Base_URL.short_url == short_url)
    row = db.execute(stmt).first()
    if row:
        return True
    return False


def get_short_url_join(db: Session, data: Base_URL) -> str:
    print(data.short_url)
    stmt = select(Base_URL).where(Base_URL.short_url == data.short_url)
    row = db.execute(stmt).first()
    if row:
        return row[0].url
    return False

def get_short_url_in_all(db: Session, short_urls: List[str]):
    stmt = select(Base_URL).where(Base_URL.short_url.in_(short_urls))
    row = db.execute(stmt).all()
    found_urls = [item.short_url for item in row]
    if len(found_urls) > 0:
        not_found_url = []
        for item_random in short_urls:
            if item_random not in found_urls:
                not_found_url.append(item_random)
        return not_found_url
    else:
        return short_urls
    
    
        


