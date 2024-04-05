from sqlalchemy.orm import Session
from app.models import OriginalUrlBase, ShortUrlBase, ShortUrl, OriginalUrl
from sqlalchemy import select
from sqlalchemy.orm.exc import NoResultFound
from typing import List
def set_original_url(db: Session, data: OriginalUrlBase):
    stmt = select(OriginalUrl).where(OriginalUrl.url == str(data.url))
    try:
        result = db.scalars(stmt).one()
    except NoResultFound:
        db_item_original = OriginalUrl(url=str(data.url))
        db.add(db_item_original)
        db.commit()
    finally:
        stmt = select(OriginalUrl).where(OriginalUrl.url == str(data.url))
        result = db.scalars(stmt).one()
        if data.short_url:
            db_item_short = ShortUrl(url_id=result.id, short_url=data.short_url)
            db.add(db_item_short)
            db.commit()
            return True
    return False


def get_short_url_in_all(db: Session, short_urls: List[str]):
    stmt = select(ShortUrl).where(ShortUrl.short_url.in_(short_urls))
    try: 
        result = db.scalars(stmt).all()
        found_urls = [item.short_url for item in result]
        not_found_url=[]        
        for item_random in short_urls:
                if item_random not in found_urls:
                    not_found_url.append(item_random)
        return not_found_url
    except NoResultFound:
        return short_urls

def get_short_url_in(db: Session, short_url: str):
    stmt = select(ShortUrl).where(ShortUrl.short_url== short_url)
    try:
        result = db.scalars(stmt).one()
        return True
    except NoResultFound:
        return False

def get_short_url_join(db: Session, data: ShortUrlBase)->str:
    inner_join_query = db.query(OriginalUrl, ShortUrl).join(ShortUrl, OriginalUrl.id == ShortUrl.url_id).filter(ShortUrl.short_url == data.short_url).first()
    if inner_join_query:
        original, short_url = inner_join_query
        return original.url
    return False