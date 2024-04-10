import logging
from fastapi import FastAPI, Depends, HTTPException
from app.createLink import CreateShortLink
from starlette.responses import RedirectResponse
from app.check import CheckUrl
from app.sessions import engine, SessionLocal
from app import model
from sqlalchemy.orm import Session

app = FastAPI(
    title="Креатор коротких урлов"
)

model.Base.metadata.create_all(bind=engine)
logging.basicConfig(level=logging.INFO)
session = Session(engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/api/url/{short_url}")
def get_short_url(short_url, db: Session = Depends(get_db)):
    shortUrl_ = 'https://' + short_url
    existing_url = db.query(model.Url).filter(model.Url.shortUrl == shortUrl_).first()
    if existing_url:
        logging.info(f"Редирект: {existing_url.url}")
        return RedirectResponse(existing_url.url)
    raise HTTPException(status_code=404, detail="Короткая ссылка не найдена")

@app.post("/api/url/")
async def add_url(url: str, short_url: str = None, db: Session = Depends(get_db)):
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
        raise HTTPException(status_code=400, detail="такой короткий url уже есть в базе, придумайте другой")
    if len(short_url) > 16:
        raise HTTPException(status_code=400, detail="короткий url должен быть не больше 8 символов")
    if CheckUrl(url) and CheckUrl(short_url):
        new_url = model.Url(url=url, shortUrl=short_url)
        db.add(new_url)
        db.commit()
        db.refresh(new_url)
        return new_url
    else:
        raise HTTPException(status_code=400, detail="Ошибка при валидации данных, ссылки не корректны")