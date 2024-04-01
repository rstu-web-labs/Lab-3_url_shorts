from http import HTTPStatus

from celery.states import SUCCESS
from fastapi import APIRouter

from app.api.schemas.cadastr import CadastrServiceResponse
from app.core.schemas import CadastrCalcResultSchema, CadastrDataSchema
from app.tasks import calculate_cadastr_data
from app.worker import celery

router = APIRouter()


@router.post("/api/url/", status_code=HTTPStatus.ACCEPTED)
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@router.get("/api/url/{short_url}")
def get_status(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}
