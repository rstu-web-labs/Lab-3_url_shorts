from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.core.db import SessionLocal
from app.schemas.url import URLCreate
from pydantic import BaseModel

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class Error(BaseModel):
    message: str

class GetUrlResponse(BaseModel):
    url: str

class CreateUrlRequest(BaseModel):
    original_url: str
    custom_url: str = None

@router.post("/url/", summary="Create Id", response_model=CreateUrlRequest, status_code=201)
def create_url(url_data: CreateUrlRequest, db: Session = Depends(get_db)):
    try:
        original_url = url_data.original_url
        return {"url": "generated_short_url"}
    except Exception as e:
        raise HTTPException(status_code=400, detail="Failed to create URL")

@router.get("/url/{short_url}/", summary="Get Url", response_model=GetUrlResponse)
def get_url(short_url: str, db: Session = Depends(get_db)):
    try:
        return {"url": "original_url"}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")
