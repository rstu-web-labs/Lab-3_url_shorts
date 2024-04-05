from app.core.logger import logger, reset_loggers
from app.core.settings import app_settings

from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.models import create_database, delete_tables
from app.short import router as router_short


@asynccontextmanager
async def lifespan(app: FastAPI):
    delete_tables()
    print("���� �������")
    create_database()
    print("���� ������ � ������")
    yield
    print("����������")


app = FastAPI(
    title="���������� �����", lifespan=lifespan
)

app.include_router(router_short)   

if not app_settings.local:
    reset_loggers()
