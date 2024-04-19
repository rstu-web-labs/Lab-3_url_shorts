from app.core.logger import logger, reset_loggers
from app.core.settings import app_settings
from fastapi import FastAPI
from app.endpoints.endp import router
from app.core.db import engine
from app.core.init_db import Base

if not app_settings.local:
    reset_loggers()
Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(router)