import uuid

import pytest
from fastapi import FastAPI
from sqlalchemy import select
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


class TestGet:

    def test_list_task_endpoint(self, client, task_in_db):
        res = client.get("/")

        assert res.status_code == 200
        assert res.json() == [{"id": task_in_db.id, "title": task_in_db.title}]


    def test_get_single_task_endpoint(self, client, task_in_db):
        res = client.get(f"/{task_in_db.id}")

        assert res.status_code == 200
        assert res.json() == {"id": task_in_db.id, "title": task_in_db.title}

    def test_get_single_task_endpoint_does_not_exist(self, client):
        res = client.get("/1")

        assert res.status_code == 404
        assert res.json() == {"msg": "No task with id 1"}


class TestPost:

    async def test_create_task(self, client, session):
        expected_title = uuid.uuid4().hex
        td = {"title": expected_title}

        res = client.post("/", json=td)

        assert res.status_code == 200
        res_data = res.json()

        task = await session.get(Task, res_data['id'])
        assert task is not None
        assert task.title == res_data['title'] == expected_title


    def test_create_task_with_invalid_data(self, client):
        res = client.post("/", json={})

        assert res.status_code == 422


    def test_create_task_with_none_title(self, client):
        res = client.post("/", json={"title": None})

        assert res.status_code == 422


    def test_create_task_with_empty_title(self, client):
        res = client.post("/", json={"title": None})

        assert res.status_code == 422


class TestPut:

    async def test_update_task(self, client, session, task_in_db):
        expected_title = uuid.uuid4().hex
        td = {"title": expected_title}

        res = client.put(f"/{task_in_db.id}", json=td)

        assert res.status_code == 200
        res_data = res.json()

        task = await session.get(Task, res_data['id'])
        assert task is not None
        assert task.id == task_in_db.id
        assert task.title == res_data['title'] == expected_title

    def test_update_task_not_found(self, client, session):
        td = {"title": uuid.uuid4().hex}

        res = client.put(f"/1", json=td)

        assert res.status_code == 404
        assert res.json() == {"msg": "No task with id 1"}
