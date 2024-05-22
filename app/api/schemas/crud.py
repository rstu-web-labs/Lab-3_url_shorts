from sqlalchemy.orm import Session
from sqlalchemy import insert
from . import url_gen, url_base
from app.models import url_map
from datetime import date

def create_db_url(db: Session, url: url_base.url_base) -> url_map.UrlMap:
    short_url = url_gen.generate_short_url(8)
    db_url = url_map.UrlMap(
        short_url=short_url, original_url=url.url, created_at=date.today()
    )
    stmt = insert(url_map.UrlMap).values(
        short_url=db_url.short_url, 
        original_url=db_url.original_url, 
        created_at=db_url.created_at
    )
    while True:
        try:
            db.execute(stmt)
            db.commit()
            break
        except:
            short_url = url_gen.generate_short_url(8)

    return db_url

def get_db_url(db: Session, short_url: url_base.url_base):
    url = db.query(url_map.UrlMap).filter(url_map.UrlMap.short_url == short_url).first()
    return url