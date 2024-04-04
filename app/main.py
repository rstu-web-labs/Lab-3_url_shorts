from app.core.logger import logger, reset_loggers
from app.core.settings import app_settings

from contextlib import asynccontextmanager
from fastapi import FastAPI
from database import create_tables, delete_tables

@asynccontextmanager
async def lifespan(app: FastAPI):
   await create_tables()
   print("База готова")
   yield
   await delete_tables()
   print("База очищена")

app = FastAPI(
 title="Укротитель Урлов"
 lifespan=lifespan
)

app.include_router(router_short)

if not app_settings.local:
    reset_loggers()
