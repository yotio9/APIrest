from contextlib import asynccontextmanager

from fastapi import FastAPI
from routes.auth import auth_rooter
from db.database import init_db


@asynccontextmanager
async def lifespan(_: FastAPI):
    await init_db()
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(auth_rooter)