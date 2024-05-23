from fastapi_users.db import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, update
from . import url_gen, url_base
from app.models.models import UrlMap, User
from datetime import date
from sqlalchemy.future import select
from app.core.db import get_session
from fastapi import Depends


async def create_db_url(db: AsyncSession, url: url_base.UrlBase, user: User) -> dict:
    short_url = url_gen.generate_short_url(8)
    while True:
        if await get_db_url(db, short_url) is None:
            break
        short_url = url_gen.generate_short_url(8)
    share_url = f"http://localhost/api/url/{short_url}"
    if user is not None:
        stmt = insert(UrlMap).values(
            short_url=short_url, original_url=url.url, created_at=date.today(), user=user.id
        )
        share_url += f"?u={user.id}"
    else:
        stmt = insert(UrlMap).values(
            short_url=short_url, original_url=url.url, created_at=date.today()
        )

    await db.execute(stmt)
    await db.commit()

    return {"url": url.url,
            "custom_url": short_url,
            "share_url": share_url
            }


async def get_db_url(db: AsyncSession, short_url: url_base.UrlBase):
    stmt = select(UrlMap).where(UrlMap.short_url == short_url)
    result = await db.execute(stmt)
    url: UrlMap = result.scalar()
    return url


async def get_user_db(session: AsyncSession = Depends(get_session)):
    yield SQLAlchemyUserDatabase(session, User)


async def verify_user(db: AsyncSession, email: str):
    stmt = update(User).where(User.email == email).values(is_verified=True)
    await db.execute(stmt)
    await db.commit()


async def count_clicks(db: AsyncSession, short_url: url_base.UrlBase):
    stmt = update(UrlMap).where(UrlMap.short_url == short_url).values(counter=UrlMap.counter + 1)
    await db.execute(stmt)
    await db.commit()
