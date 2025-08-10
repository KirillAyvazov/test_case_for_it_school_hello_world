from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from src.router.hero import router as hero_router
from src.database.db_connect import create_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    yield


app = FastAPI(title="Test case for IT School Hello World", lifespan=lifespan)
app.include_router(hero_router)
