from typing import AsyncGenerator

from sqlalchemy import text
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base

from app.core.logger import logger
from app.core.settings import app_settings

engine = create_async_engine(app_settings.postgres_database_url)
SessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

Base = declarative_base()


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session


async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def check_db_connection() -> bool:
    async with SessionLocal() as session:
        try:
            return bool(await session.execute(text("SELECT 1")))
        except ConnectionError as error:
            logger.critical(f"Postgres connection error: {error}")
    return False
