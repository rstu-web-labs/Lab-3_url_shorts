from fastapi import FastAPI
from app.models.endpoints import router as endpoints_router

app = FastAPI(title="Укоротитель Урлов", version="0.1.0")

# Подключаем роутер к основному приложению
app.include_router(endpoints_router, prefix="/api")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
