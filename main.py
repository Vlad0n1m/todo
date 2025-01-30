from fastapi import FastAPI
import logging
import uvicorn
from contextlib import asynccontextmanager
from app.routers.task import router as task_router
from app.database.db import setup_database

logging.basicConfig(
    level=logging.INFO,
    filename="logs.log",
    format="%(levelname)s (%(asctime)s): %(message)s (Line: %(lineno)d [%(filename)s])",
    datefmt="%d/%m/%Y %I:%M:%S",
    encoding='utf-8',
)


@asynccontextmanager 
async def lifespan(app: FastAPI):
    await setup_database()
    yield


app = FastAPI(title="Todo api", lifespan=lifespan)

app.include_router(task_router)


@app.get("/")
def home():
    logging.info("Запросили корневой эндпоинт")
    return "Иди на /docs"


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", reload=True)
