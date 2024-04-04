from app.schemas.requests import Item

from app.models.url_map import UrlMap
from sqlalchemy import select
from app.core.db import SessionLocal

def get_short_url(data: Item):
    return "bbbbb"

def get_url(short_url: str) -> str:
    session = SessionLocal()
    stnt = select(UrlMap).where(UrlMap.short_url == short_url)
    result = session.execute(stnt)
    obj = result.scalar()
    session.close()
    if obj:
        return obj.url
    return None