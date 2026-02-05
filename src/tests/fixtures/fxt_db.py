from contextlib import asynccontextmanager

import pytest
import pytest_asyncio
from sqlalchemy import DDL
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from base import BaseModel


@pytest_asyncio.fixture(scope="session", loop_scope="session")
async def engine():
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as conn:
        await conn.execute(DDL("PRAGMA foreign_keys = ON;"))
        await conn.run_sync(BaseModel.metadata.create_all)

    yield engine

    await engine.dispose()


@pytest.fixture
async def make_session(engine):

    AsyncSession = async_sessionmaker(
        expire_on_commit=False, join_transaction_mode="create_savepoint"
    )

    @asynccontextmanager
    async def _mk_session():
        async with AsyncSession(bind=conn) as s:
            yield s

    async with engine.connect() as conn:
        await conn.begin_nested()
        yield _mk_session


@pytest.fixture
async def session(make_session):
    async with make_session() as s:
        yield s
