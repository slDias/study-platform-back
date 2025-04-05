import pytest

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from starlette.testclient import TestClient

from models import Base
from main import app


@pytest.fixture
async def session():
    engine = create_async_engine("sqlite+aiosqlite://")

    async with engine.connect() as conn:
        await conn.run_sync(Base.metadata.create_all)

    AsyncSession = async_sessionmaker(engine, expire_on_commit=False)

    async with AsyncSession() as session:
        yield session


@pytest.fixture
def client():
    yield TestClient(app)
