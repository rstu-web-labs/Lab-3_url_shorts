from fastapi import FastAPI
from app.models.endpoints import router as endpoints_router
from app.core.db import Base
from app.core.db import engine
from app.core.db import check_db_connection
from app.models.url_map import UrlMap


app = FastAPI(title="Укоротитель Урлов", version="0.1.0")

Base.metadata.create_all(bind=engine)
# Подключаем роутер к основному приложению
app.include_router(endpoints_router, prefix="/api")

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)
