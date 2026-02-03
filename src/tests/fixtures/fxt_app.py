from typing import AsyncGenerator

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from dependencies import get_session
from main import app as main_app


@pytest.fixture
async def empty_app(make_session) -> AsyncGenerator[FastAPI]:
    fastapi_app = FastAPI()
    async with make_session() as s:
        _override_dependencies(fastapi_app, s)
        yield fastapi_app


@pytest.fixture
async def client(make_session):
    async with make_session() as s:
        _override_dependencies(main_app, s)
        yield TestClient(main_app)


def _override_dependencies(app: FastAPI, session) -> None:
    def _get_session():
        return session

    app.dependency_overrides[get_session] = _get_session
