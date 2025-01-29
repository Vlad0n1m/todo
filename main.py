from fastapi import FastAPI
import uvicorn
from contextlib import asynccontextmanager
from app.routers.task import router as task_router
from app.database.db import setup_database


@asynccontextmanager
async def lifespan(app: FastAPI):
    await setup_database()
    yield

app = FastAPI(title="Todo api", lifespan=lifespan)

app.include_router(task_router)


if __name__ == "__main__":
    uvicorn.run("main:app",host="0.0.0.0", reload=True)
