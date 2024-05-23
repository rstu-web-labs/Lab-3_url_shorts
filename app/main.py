from app.api.auth.auth import fastapi_users, auth_backend
from app.api.schemas.user_schemas import UserRead, UserCreate
from app.core.logger import reset_loggers
from app.core.settings import app_settings
from app.core.db import create_db_and_tables
from fastapi import FastAPI, Depends, HTTPException
from app.api.endpoints.endpoints import main_router, email_conf
from app.models.models import User
import asyncio

if not app_settings.local:
    reset_loggers()

app = FastAPI(title="Укоротитель Урлов")

asyncio.create_task(create_db_and_tables())

app.include_router(
    main_router,
    prefix="/api",
    tags=["url_short"]
)

app.include_router(
    email_conf,
    prefix="/api",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/api/users",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/api/users",
    tags=["auth"],
)

current_user = fastapi_users.current_user()


@app.get("/protected-route")
def protected_route(user: User = Depends(current_user)):
    if user is None:
        raise HTTPException(status_code=500)
    return f"Hello, {user.username}"


@app.get("/unprotected-route")
def unprotected_route():
    return f"Hello, someone!"
