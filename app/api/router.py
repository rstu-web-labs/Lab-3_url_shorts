from fastapi import APIRouter

from app.api.endpoints import rout

main_router = APIRouter()

main_router.include_router(rout,  prefix='/api/url')

