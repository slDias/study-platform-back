import pytest
import pytest_asyncio
from fastapi import FastAPI

from fastapi.testclient import TestClient
from sqlalchemy import DDL
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from base import BaseModel
from dependencies import get_session
from main import app as main_app


@pytest.fixture
def empty_app(session) -> FastAPI:
    fastapi_app = FastAPI()
    _override_dependencies(fastapi_app, session)

    return fastapi_app


@pytest_asyncio.fixture(scope="session", loop_scope="session")
async def engine():
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")

    async with engine.connect() as conn:
        await conn.run_sync(BaseModel.metadata.create_all)
        await conn.execute(DDL("PRAGMA foreign_keys = ON"))

    yield engine

@pytest.fixture
async def session(engine):
    AsyncSession = async_sessionmaker(expire_on_commit=False, join_transaction_mode="create_savepoint")

    async with engine.connect() as conn:
        await conn.begin_nested()
        async with AsyncSession(bind=conn) as s:
            yield s

@pytest.fixture
def client(session):
    _override_dependencies(main_app, session)
    return TestClient(main_app)

def _override_dependencies(app: FastAPI, session) -> None:
    def _get_session():
        return session

    app.dependency_overrides[get_session] = _get_session
