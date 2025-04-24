from contextlib import asynccontextmanager

import pytest
import pytest_asyncio

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from base import BaseModel


@pytest_asyncio.fixture(scope="session", loop_scope="session")
async def engine():
    engine = create_async_engine("postgresql+psycopg://postgres:postgres@0.0.0.0:5432/test")

    async with engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.create_all)

    yield engine


@pytest.fixture
async def make_session(engine):

    @asynccontextmanager
    async def _mk_session():
        AsyncSession = async_sessionmaker(expire_on_commit=False, join_transaction_mode="create_savepoint")

        async with engine.connect() as conn:
            await conn.begin_nested()
            async with AsyncSession(bind=conn) as s:
                yield s

    return _mk_session

@pytest.fixture
async def session(make_session):
     async with make_session() as s:
        yield s
