import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from dependencies import get_session
from main import app as main_app


@pytest.fixture
def empty_app(session) -> FastAPI:
    fastapi_app = FastAPI()
    _override_dependencies(fastapi_app, session)

    return fastapi_app


@pytest.fixture
def client(session):
    _override_dependencies(main_app, session)
    return TestClient(main_app)


def _override_dependencies(app: FastAPI, session) -> None:
    def _get_session():
        session.expire_all()
        return session

    app.dependency_overrides[get_session] = _get_session
