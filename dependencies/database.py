from typing import Annotated

from fastapi.params import Depends
from sqlalchemy import DDL
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncEngine

from base import BaseModel

# todo create the engine based on env vars
engine = create_async_engine("sqlite+aiosqlite:///:memory:")
AsyncSession = async_sessionmaker(engine, expire_on_commit=False)


async def set_up(engine: AsyncEngine) -> None:
    async with engine.connect() as conn:
        await conn.run_sync(BaseModel.metadata.create_all)
        await conn.execute(DDL("PRAGMA foreign_keys = ON"))


async def get_session() -> "AsyncSession":
    async with AsyncSession() as session:
        yield session

SessionDep = Annotated[AsyncSession, Depends(get_session)]
