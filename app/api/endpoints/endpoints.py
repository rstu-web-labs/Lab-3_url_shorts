import itsdangerous
import validators
from app.api.auth.auth import fastapi_users
from http import HTTPStatus
from fastapi import APIRouter, Depends
from fastapi.responses import RedirectResponse
from app.api.schemas.url_base import UrlBase
from app.api.schemas.crud import create_db_url, get_db_url, verify_user, count_clicks
from app.core.db import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from app.config import SECRET
from app.models.models import User

main_router = APIRouter()
email_conf = APIRouter()


@main_router.post("/url")
async def create_short_url(
        url: UrlBase,
        db: AsyncSession = Depends(get_session),
        user: User = Depends(fastapi_users.current_user())
):
    if not validators.url(url.url):
        return HTTPStatus.BAD_REQUEST
    db_url = await create_db_url(db, url, user)
    return db_url


@main_router.get("/url/{short_url}")
async def forward_to_target_url(short_url, db: AsyncSession = Depends(get_session)):
    url = await get_db_url(db, short_url)
    if url is None:
        return HTTPStatus.NOT_FOUND
    await count_clicks(db, short_url)
    return RedirectResponse(url.original_url)


@email_conf.get("/users/email-verification/{token}")
async def verify_email(token: str, db: AsyncSession = Depends(get_session)):
    serializer = itsdangerous.URLSafeTimedSerializer(SECRET)
    try:
        email = serializer.loads(token, salt=SECRET, max_age=3600)
        await verify_user(db, email)
        return "Вы успешно подтвердили свой email!"
    except itsdangerous.BadData:
        return HTTPStatus.BAD_REQUEST
