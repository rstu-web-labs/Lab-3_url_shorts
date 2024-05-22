import validators
from http import HTTPStatus
from fastapi import APIRouter, Depends
from fastapi.responses import RedirectResponse
from app.api.schemas.url_base import url_base
from app.api.schemas.crud import create_db_url, get_db_url
from app.core.db import get_session, check_db_connection
from sqlalchemy.orm import Session

router = APIRouter()

@router.post("/url")
def create_short_url(url: url_base, db: Session = Depends(get_session)):
    if not validators.url(url.url):
        return HTTPStatus.BAD_REQUEST
    check_db_connection()
    db_url = create_db_url(db, url)
    return db_url

@router.get("/url/{short_url}")
def forward_to_target_url(short_url: str, db: Session = Depends(get_session)):
    check_db_connection()
    url = get_db_url(db, short_url)
    if url == None:
        return HTTPStatus.NOT_FOUND
    return RedirectResponse(url.original_url)
