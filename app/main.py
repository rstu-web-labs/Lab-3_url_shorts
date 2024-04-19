from fastapi import FastAPI
import uvicorn

from app.core.logger import logger, reset_loggers
from app.core.settings import app_settings
from app.api import router
from app.models import create_database, delete_tables

app = FastAPI()
app.include_router(router)
create_database()

if not app_settings.local:
    reset_loggers()

if __name__ == "__main__":
    uvicorn.run("app.main:app", port=8000, host='0.0.0.0', reload=True)
    