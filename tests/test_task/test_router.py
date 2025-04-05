import uuid

import pytest
from fastapi import FastAPI
from starlette.testclient import TestClient

from dependencies import get_session
from task.model import Task
from task.router import task_router
from task.schema import TaskSchema


@pytest.fixture()
async def client(session):
    def _get_session():
        return session

    app = FastAPI()
    app.include_router(task_router)
    app.dependency_overrides[get_session] = _get_session

    yield TestClient(app)


@pytest.fixture()
async def task_in_db(session):
    task = Task(title=uuid.uuid4().hex)
    session.add(task)
    await session.commit()
    return task


def test_list_task_endpoint(client, task_in_db):
    task_serialized = task_in_db.to_dict()

    res = client.get("/")

    assert res.status_code == 200
    assert res.json() == [task_serialized]
