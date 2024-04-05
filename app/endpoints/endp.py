from fastapi import APIRouter, HTTPException
from app.models.url_map import Post
from app.schemas.url import UrlOut, UrlIn
from app.core.db import SessionLocal
from sqlalchemy.exc import IntegrityError
from sqlalchemy import insert
import random
import string
from datetime import date
from fastapi.responses import RedirectResponse

router = APIRouter()

def generate_short_url(length: int = 8):
    short_url = ''
    while len(short_url) < length:
        short_url += random.choice(string.ascii_letters + string.digits)
    return short_url

@router.post("/api/url/", response_model=UrlOut)
async def create_url(url_in: UrlIn):
    session = SessionLocal()
    print(session)

    if not url_in.short_url:
        short_url = generate_short_url()
        while session.query(Post).filter(Post.short_url == short_url).first():
            short_url = generate_short_url()
    else:
        short_url = url_in.short_url

    url = Post(short_url=short_url, url=url_in.url, created_at=date.today())

    try:
        stmt = insert(Post).values(url=url_in.url, short_url=short_url, created_at=date.today())
        result = session.execute(stmt)
        print(result)
        session.commit()
        # session.add(url)
        # session.commit()
    except IntegrityError as err:
        print(str(err))
        session.rollback()
        raise HTTPException(status_code=400, detail="Failed to create URL")

    return UrlOut(short_url=url.short_url, url=url.url, created_at=date.today())

@router.get("/api/url/{short_url}", response_model=UrlOut)
async def get_url(short_url: str):
    session = SessionLocal()

    url = session.query(Post).filter(Post.short_url == short_url).first()

    if not url:
        raise HTTPException(status_code=404, detail="URL not found")

    return RedirectResponse(url.url)