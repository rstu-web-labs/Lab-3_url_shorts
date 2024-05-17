from app.core.logger import reset_loggers
from app.core.settings import app_settings
from app.core.db import Base, engine
from fastapi import FastAPI
from app.api.endpoints.endpoints import router


if not app_settings.local:
    reset_loggers()

app = FastAPI(title='Укоротитель Урлов')

Base.metadata.create_all(bind=engine)

app.include_router(router, prefix="/api")

