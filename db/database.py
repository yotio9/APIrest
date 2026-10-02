import os
from typing import Annotated

from dotenv import load_dotenv
from fastapi import  Depends
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase
import os

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")


engine = create_async_engine(DATABASE_URL, echo=True)

sessionlocal=async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)    

class Base(DeclarativeBase):
    pass

async def init_db():
   async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
async def get_db() :
    db = sessionlocal()
    try:
        yield db
    finally:
        await db.close()


db_dependency= Annotated[AsyncSession, Depends(get_db)]

