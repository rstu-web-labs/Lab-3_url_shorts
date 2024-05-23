from fastapi import APIRouter

from app.api.endpoints import cadastr_router



app = FastAPI()

@app.get("/")
def read_root():
    return "Welcome to the URL shortener API :)"