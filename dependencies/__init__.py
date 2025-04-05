from contextlib import asynccontextmanager
from typing import Annotated, Any, AsyncGenerator

from fastapi import FastAPI
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession

from models import Base

engine = create_async_engine("sqlite+aiosqlite://")
open_session = async_sessionmaker(engine, expire_on_commit=False)


@asynccontextmanager
async def lifespan(_: FastAPI):
    async with engine.connect() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_session() -> AsyncGenerator[AsyncSession, Any]:
    async with open_session() as session:
        yield session

SessionDep = Annotated[AsyncSession, Depends(get_session)]
