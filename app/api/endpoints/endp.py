from fastapi import APIRouter

from app.api.schema import ShortURL
from app.url import generate_short_link
from app.models import get_original_url
from app.core.db import get_session

router = APIRouter()

@router.get('/{short_url}', tags=['Перейти по новой ссылке'])
def get(short_url:str):
    return get_original_url(short_url, get_session().__next__())

@router.post('/', tags=['Создать короткую ссылку'])
def post(url:str)->ShortURL:
    return generate_short_link(url)

