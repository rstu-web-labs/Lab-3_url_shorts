from fastapi import APIRouter, Depends
from typing import Annotated
from app.models import OriginalUrlBase, ShortUrlBase
from app.short.crud import set_original_url, get_short_url_in, get_short_url_in_all,get_short_url_join
from app.core import get_session
from sqlalchemy.orm import Session
from app.short.RandomLink import RandomLink

from fastapi.responses import RedirectResponse

router = APIRouter(
    prefix="/api/url",
    tags=["default"]
)

@router.get("/{short_url}")
def short_url(short_url: Annotated[ShortUrlBase,Depends()], db: Session = Depends(get_session)):
    if get_short_url_join(db,short_url):
        return RedirectResponse(get_short_url_join(db,short_url))
    return {"Ошибка": "Короткая ссылка не найдена"}


@router.post("")
def original_url(url):
    
    # db = get_session
    print(url)
    
    if url:
        if get_short_url_in(db, url):
            return {"Ошибка": "Придумайте другую короткую сслыку или оставьте поле пустым"}
        else:
            set_original_url(db,url)
    else: 
        generate_urls = get_short_url_in_all(db, RandomLink.array_random_links())
        if len(generate_urls)>0: 
            url.short_url=generate_urls[0]
            set_original_url(db, url)
    return url