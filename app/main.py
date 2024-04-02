from app.core.logger import logger, reset_loggers
from app.core.settings import app_settings

if not app_settings.local:
    reset_loggers()
