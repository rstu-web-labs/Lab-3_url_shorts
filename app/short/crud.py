from sqlalchemy.orm import Session
from app.models import OriginalUrlBase, ShortUrlBase, OriginalUrl
from sqlalchemy import select, insert
from sqlalchemy.orm.exc import NoResultFound
from typing import List


def set_original_url(db: Session, data: OriginalUrlBase) -> bool:
    stmt = insert(OriginalUrl).values(url=str(data.url), short_url=str(data.short_url))
    db.execute(stmt)
    db.commit()
    return True


def get_short_url_in(db: Session, short_url: str):
    stmt = select(OriginalUrl).where(OriginalUrl.short_url == short_url)
    row = db.execute(stmt).first()
    if row:
        return True
    return False


def get_short_url_join(db: Session, data: ShortUrlBase) -> str:
    print(data.short_url)
    stmt = select(OriginalUrl).where(OriginalUrl.short_url == data.short_url)
    row = db.execute(stmt).first()
    if row:
        return row[0].url
    return False


def get_short_url_in_all(db: Session, short_urls: List[str]):
    stmt = select(OriginalUrl).where(OriginalUrl.short_url.in_(short_urls))
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
