from app.core.logger import logger, reset_loggers
from app.core.settings import app_settings
from app.core.db import engine, get_session
from fastapi import Depends, APIRouter
from app.models.schema import  Forma_Base_URL, Forma_Short_URL
from sqlalchemy.orm import Session
from app.query.queryDB import check_originality_short_link, add_short_and_base_link, get_base_url_from_short_url
from typing import Annotated
from fastapi.responses import RedirectResponse

router = APIRouter(prefix='/router1')

@router.post('/')
def add_data_in_DB(data: Annotated[Forma_Base_URL,Depends()], db: Session = Depends(get_session)):
    if check_originality_short_link(data.short_URL, db):
        return {"Ошибка": "Значение не уникально"}
    else:
        add_short_and_base_link(data, db)
    return data

@router.get('/{short_URL}')
def short_in_base_transition(short_URL: Annotated[Forma_Short_URL,Depends()], db: Session = Depends(get_session)):
    if get_base_url_from_short_url(short_URL, db):
        return RedirectResponse(get_base_url_from_short_url(short_URL, db))
    else:
        return {"Ошибка": "Значение не найдено"}  