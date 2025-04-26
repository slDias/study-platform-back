from contextlib import asynccontextmanager

import pytest
import pytest_asyncio
from psycopg.errors import DuplicateDatabase
from sqlalchemy import text
from sqlalchemy.exc import ProgrammingError

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from base import BaseModel


@pytest_asyncio.fixture(scope="session", loop_scope="session")
async def engine():
    default_db_engine = create_async_engine("postgresql+psycopg://postgres:postgres@0.0.0.0:5432/")

    try:
        async with default_db_engine.connect() as conn:
            await conn.execution_options(isolation_level="AUTOCOMMIT")
            await conn.execute(text("create database test"))
    except ProgrammingError as e:
        if not isinstance(e.orig, DuplicateDatabase):
            raise

    engine = create_async_engine("postgresql+psycopg://postgres:postgres@0.0.0.0:5432/test")
    async with engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.create_all)

    yield engine

    await engine.dispose()

    async with default_db_engine.connect() as conn:
        await conn.execution_options(isolation_level="AUTOCOMMIT")
        await conn.execute(text("drop database test"))


@pytest.fixture
async def make_session(engine):
    @asynccontextmanager
    async def _mk_session():
        async with AsyncSession(bind=conn) as s:
            yield s

    AsyncSession = async_sessionmaker(expire_on_commit=False, join_transaction_mode="create_savepoint")

    async with engine.connect() as conn:
        await conn.begin_nested()
        yield _mk_session


@pytest.fixture
async def session(make_session):
     async with make_session() as s:
        yield s
