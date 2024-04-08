from datetime import date
from sqlalchemy import insert
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import RedirectResponse
from app.schemas.url import URLCreate, Urls, get_db, generate_short_url
from app.models.url_map import UrlMap



router = APIRouter()


@router.post("/api/url/", response_model=Urls)
async def create_url(url_in: URLCreate, db: Session = Depends(get_db)):
    if not url_in.short_url:
        short_url = generate_short_url()
        while db.query(UrlMap).filter(UrlMap.short_url == short_url).first():
            short_url = generate_short_url()
    else:
        short_url = url_in.short_url

    url = UrlMap(short_url=short_url, url=url_in.original_url, created_at=date.today())

    try:
        stmt = insert(UrlMap).values(url=url_in.original_url, short_url=short_url, created_at=date.today())
        result = db.execute(stmt)
        db.commit()
    except IntegrityError as err:
        print(str(err))
        db.rollback()
        raise HTTPException(status_code=400, detail="Failed to create URL")

    print(url.id)
    return {"url": url.url, "short_url": url.short_url}

@router.get("/url/{short_url}/", summary="Get Url")
def get_url(short_url: str, db: Session = Depends(get_db)):
    url_map = db.query(UrlMap).filter(UrlMap.short_url == short_url).first()
    return RedirectResponse(url_map.url)
