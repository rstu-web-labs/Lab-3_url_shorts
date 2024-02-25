from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncAttrs, AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from app.core.logger import logger
from app.core.settings import app_settings

Base = type("Base", (AsyncAttrs, DeclarativeBase), {})
engine = create_async_engine(app_settings.postgres_database_url)
AsyncSessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_async_session():
    async with AsyncSessionLocal() as session:
        yield session


async def check_db_connection() -> bool:
    async for session in get_async_session():
        try:
            return bool(await session.execute(text("SELECT 1")))
        except ConnectionError as error:
            logger.critical(f"Postgres connection error: {error}")
        finally:
            await session.close()
        return False
