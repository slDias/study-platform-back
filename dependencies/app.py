from contextlib import asynccontextmanager

from fastapi import FastAPI

from . import database


@asynccontextmanager
async def lifespan(_: FastAPI):
    await database.set_up()
    yield