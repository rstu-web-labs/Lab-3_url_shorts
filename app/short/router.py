from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated
from app.models import OriginalUrlBase, ShortUrlBase
from app.short.crud import set_original_url, get_short_url_in, get_short_url_in_all, get_short_url_join
from app.core import get_session
from sqlalchemy.orm import Session
from app.short.RandomLink import RandomLink

from fastapi.responses import RedirectResponse

router = APIRouter(prefix="/api/url", tags=["default"])


@router.get("/{short_url}")
def short_url(short_url: Annotated[ShortUrlBase, Depends()], db: Session = Depends(get_session)):
    if get_short_url_join(db, short_url):
        print(get_short_url_join(db, short_url))
        return RedirectResponse(get_short_url_join(db, short_url))
    # return {"Ошибка": "Короткая ссылка не найдена"}
    raise HTTPException(
        status_code=303,
        detail="Короткая ссылка не найдена",
        headers={"X-Error": "There goes my error"},
    )


@router.post("")
def original_url(data: Annotated[OriginalUrlBase, Depends()], db: Session = Depends(get_session)):
    if data.short_url:
        if get_short_url_in(db, data.short_url):
            raise HTTPException(
                status_code=418,
                detail="Придумайте другую короткую сслыку или оставьте поле пустым",
                headers={"X-Error": "There goes my error"},
            )
        else:
            set_original_url(db, data)
    else:
        generate_urls = get_short_url_in_all(db, RandomLink.array_random_links())
        if len(generate_urls) > 0:
            data.short_url = generate_urls[0]
            set_original_url(db, data)
        else:
            generate_urls = get_short_url_in_all(db, RandomLink.array_random_links())
    return data
