import logging
from fastapi import FastAPI, Depends, HTTPException
from app.createLink import CreateShortLink
from starlette.responses import RedirectResponse
from app.check import CheckUrl
from app.main.session import engine, SessionLocal
from app.main import model
from sqlalchemy.orm import Session

app = FastAPI(
    title="urlurlurl"
)
model.Base.metadata.create_all(bind=engine)
logging.basicConfig(level=logging.INFO)
session = Session(engine)
def GetDB():
    DB = SessionLocal()
    try:
        yield DB
    finally:
        DB.close()

@app.get("/api/url/{short_url}")
def get_short_url(short_url, db: Session = Depends(GetDB)):
    shortUrl_ = 'https://' + short_url
    existing_url = db.query(model.Url).filter(model.Url.shortUrl == shortUrl_).first()
    if existing_url:
        logging.info(f"Переходим на: {existing_url.url}")
        return RedirectResponse(existing_url.url)
    raise HTTPException(status_code=404, detail="Короткой ссылки не существует")

@app.post("/api/url/")
async def add_url(url: str, short_url: str = None, db: Session = Depends(GetDB)):
    logging.info(f"Get to request: {url}, {short_url}")
    if short_url is None:
        existing_url = db.query(model.Url).filter(model.Url.url == url).first()
        if existing_url:
            short_url = existing_url.shortUrl
            return model.Url(url=url, short_url=short_url)
        else:
            while True:
                short_url = CreateShortLink()
                if not db.query(model.Url).filter(model.Url.shortUrl == short_url).first():
                    break
    if (db.query(model.Url).filter(model.Url.shortUrl == short_url).first()):
        raise HTTPException(status_code=400, detail="введенный url уже есть")
    if len(short_url) > 16:
        raise HTTPException(status_code=400, detail="short url должен быть менее 9 символов")
    if CheckUrl(url) and CheckUrl(short_url):
        newUrl = model.Url(url=url, shortUrl=short_url)
        db.add(newUrl)
        db.commit()
        db.refresh(newUrl)
        return newUrl
    else:
        raise HTTPException(status_code=400, detail="Ошибка проверки urlов, ссылки не корректны")