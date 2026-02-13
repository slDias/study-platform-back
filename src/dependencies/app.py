import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI

from . import database, schedule_runner


@asynccontextmanager
async def lifespan(_: FastAPI):
    await database.set_up(database.engine)
    loop = asyncio.get_event_loop()
    loop.create_task(schedule_runner.run())
    yield
