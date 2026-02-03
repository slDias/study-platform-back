from os import environ
from typing import Annotated, AsyncGenerator

from fastapi.params import Depends
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from base import BaseModel

engine = create_async_engine(environ["DB_URL"])
AsyncSessionMaker = async_sessionmaker(engine, expire_on_commit=False)


async def set_up(engine: AsyncEngine) -> None:
    async with engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.create_all)


async def get_session() -> AsyncGenerator[AsyncSession]:
    async with AsyncSessionMaker() as session:
        yield session


SessionDep = Annotated[AsyncSession, Depends(get_session)]
