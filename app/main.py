import logging
from fastapi import FastAPI, Depends, HTTPException
from app.generate.generate import generate_short_link
from starlette.responses import RedirectResponse
from app.validation.validation import validate_url
from app.db.sessions import engine, SessionLocal
from app.db import model
from sqlalchemy.orm import Session

app = FastAPI(
    title="Короткий урл"
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
    Short_url = 'https://' + short_url
    existing_url = db.query(model.Url).filter(model.Url.shortUrl == Short_url).first()
    if existing_url:
        logging.info(f"Перенаправляем: {existing_url.url}")
        return RedirectResponse(existing_url.url)
    raise HTTPException(status_code=404, detail="Введённая короткая ссылка - не найдена")

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
                short_url = generate_short_link()
                if not db.query(model.Url).filter(model.Url.shortUrl == short_url).first():
                    break
    if (db.query(model.Url).filter(model.Url.shortUrl == short_url).first()):
        raise HTTPException(status_code=400, detail="введённый короткий url уже есть в БД")
    if len(short_url) > 16:
        raise HTTPException(status_code=400, detail="длина короткого url <= 8 символов")
    if validate_url(url) and validate_url(short_url):
        new_url = model.Url(url=url, shortUrl=short_url)
        db.add(new_url)
        db.commit()
        db.refresh(new_url)
        return new_url
    else:
        raise HTTPException(status_code=400, detail="Ошибка валидации данных, ссылки не корректны")