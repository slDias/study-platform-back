import pytest
from fastapi import FastAPI

from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from base import BaseModel
from dependencies import get_session
from main import app as main_app


@pytest.fixture
def empty_app(session) -> FastAPI:
    fastapi_app = FastAPI()
    _override_dependencies(fastapi_app, session)

    return fastapi_app

@pytest.fixture
async def session():
    engine = create_async_engine("sqlite+aiosqlite://")

    async with engine.connect() as conn:
        await conn.run_sync(BaseModel.metadata.create_all)

    AsyncSession = async_sessionmaker(engine, expire_on_commit=False)

    async with AsyncSession() as session:
        yield session

@pytest.fixture
def client(session):
    _override_dependencies(main_app, session)
    return TestClient(main_app)

def _override_dependencies(app: FastAPI, session) -> None:
    def _get_session():
        return session

    app.dependency_overrides[get_session] = _get_session
