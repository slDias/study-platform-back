from sqlalchemy import inspect
from sqlalchemy.ext.asyncio import create_async_engine

from base import BaseModel
from dependencies.database import set_up


async def test_set_up():
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")

    await set_up(engine)

    async with engine.connect() as connection:
        tables_in_db = await connection.run_sync(lambda c: inspect(c).get_table_names())
        assert all(t in tables_in_db for t in BaseModel.metadata.tables.keys())
