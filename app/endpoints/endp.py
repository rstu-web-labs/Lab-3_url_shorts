from fastapi import APIRouter, HTTPException
from app.models.url_map import Post
from app.schemas.url import UrlOut, UrlIn
from app.core.db import SessionLocal
from sqlalchemy.exc import IntegrityError
import random
import string

router = APIRouter()

@router.post("/api/url/", response_model=UrlOut)
async def create_url(url_in: UrlIn):
    session = SessionLocal()

    if session.query(Post).filter(Post.url == url_in.url).first():
        raise HTTPException(status_code=400, detail="URL already exists")

    while True:
        short_url = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
        if not session.query(Post).filter(Post.short_url == short_url).first():
            break

    url = Post(short_url=short_url, url=url_in.url)


    try:
        session.add(url)
        session.commit()
    except IntegrityError:
        session.rollback()
        raise HTTPException(status_code=400, detail="Failed to create URL")

    return UrlOut(short_url=url.short_url, url=url.url)

@router.get("/api/url/{short_url}", response_model=UrlOut)
async def get_url(short_url: str):
    session = SessionLocal()

    url = session.query(Post).filter(Post.short_url == short_url).first()

    if not url:
        raise HTTPException(status_code=404, detail="URL not found")

    return UrlOut(short_url=url.short_url, url=url.url)