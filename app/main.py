from app.core.logger import logger, reset_loggers
from app.core.settings import app_settings
from fastapi import FastAPI
from app.models.url_map import create_table_database
from contextlib import asynccontextmanager
from app.router import router as ttt

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_table_database()
    print('База Запущена') 

    yield
    print('Все сламалося. Больше не работает')


app = FastAPI(
    title='Что то там... Ссылки',
    lifespan=lifespan
)

app.include_router(ttt)

if not app_settings.local:
    reset_loggers()
