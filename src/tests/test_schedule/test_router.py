import uuid

import pytest
from starlette.testclient import TestClient

from schedule import schedule_router, Schedule
from task import Task


@pytest.fixture
def client(empty_app):
    empty_app.include_router(schedule_router)
    return TestClient(empty_app)


class TestGet:
    def test_list_schedule(self, client, schedule_in_db):
        res = client.get("/")

        assert res.status_code == 200
        assert res.json() == [{
            "id": schedule_in_db.id,
            "task_id": schedule_in_db.task_id,
            "task": {"id": schedule_in_db.task_id, "title": schedule_in_db.task.title},
            "cron": schedule_in_db.cron,
            "time_limit": schedule_in_db.time_limit
        }]

    def test_get_single_schedule(self, client, schedule_in_db):
        res = client.get(f"/{schedule_in_db.id}")

        assert res.status_code == 200
        assert res.json() == {
            "id": schedule_in_db.id,
            "task_id": schedule_in_db.task_id,
            "task": {"id": schedule_in_db.task_id, "title": schedule_in_db.task.title},
            "cron": schedule_in_db.cron,
            "time_limit": schedule_in_db.time_limit
        }

    def test_get_single_schedule_does_not_exist(self, client):
        res = client.get("/1")

        assert res.status_code == 404
        assert res.json() == {"msg": "No schedule with id 1"}


class TestPost:
    async def test_create_schedule(self, client, session, task_in_db):
        data = {"task_id": task_in_db.id, "cron": "0 0 * * 1", "time_limit": 24}

        res = client.post("/", json=data)

        assert res.status_code == 200
        s = await session.get(Schedule, res.json()['id'])
        assert res.json() == {
            "id": s.id,
            "task_id": task_in_db.id,
            "task": {"id": task_in_db.id, "title": task_in_db.title},
            "cron": "0 0 * * 1",
            "time_limit": 24
        }

    def test_create_schedule_task_does_not_exist(self, client):
        data = {"task_id": 1, "cron": "0 0 * * 1", "time_limit": 24}

        res = client.post("/", json=data)

        assert res.status_code == 400
        assert res.json() == {"msg": "Specified task 1 does not exist"}

    async def test_create_schedule_with_task_object(self, client, session, task_in_db):
        data = {"task": {"id": task_in_db.id, "title": task_in_db.title}, "cron": "0 0 * * 1", "time_limit": 24}

        res = client.post("/", json=data)

        assert res.status_code == 200
        s = await session.get(Schedule, res.json()['id'])
        assert res.json() == {
            "id": s.id,
            "task_id": task_in_db.id,
            "task": {"id": task_in_db.id, "title": task_in_db.title},
            "cron": "0 0 * * 1",
            "time_limit": 24
        }

    def test_create_schedule_task_with_invalid_cron(self, client, task_in_db):
        data = {"task_id": task_in_db.id, "cron": "abc", "time_limit": 24}

        res = client.post("/", json=data)

        assert res.status_code == 422

    def test_create_schedule_task_with_invalid_time_limit(self, client, task_in_db):
        data = {"task_id": task_in_db.id, "cron": "0 0 * * 1", "time_limit": 0}

        res = client.post("/", json=data)

        assert res.status_code == 422


class TestPut:
    
    async def test_update_schedule(self, client, session, schedule_in_db):
        new_task = Task(title=uuid.uuid4().hex)
        session.add(new_task)
        await session.commit()
        expected_task_id = new_task.id
        expected_cron = "0 0 * * 2"
        expected_time_limit = 22
        data = {"task_id": expected_task_id, "cron": expected_cron, "time_limit": expected_time_limit}

        res = client.put(f"/{schedule_in_db.id}", json=data)

        assert res.status_code == 200
        await session.refresh(schedule_in_db)
        assert res.json() == {
            "id": schedule_in_db.id,
            "task_id": expected_task_id,
            "task": {"id": new_task.id, "title": new_task.title},
            "cron": expected_cron,
            "time_limit": expected_time_limit
        }

    def test_update_schedule_with_non_existent_task(self, client, schedule_in_db):
        data = {"task_id": 999, "cron": "0 0 * * 2", "time_limit": 22}

        res = client.put(f"/{schedule_in_db.id}", json=data)

        assert res.status_code == 400
        assert res.json() == {"msg": f"Specified task 999 does not exist"}

    def test_update_non_existent_schedule(self, client, task_in_db):
        data = {"task_id": task_in_db.id, "cron": "0 0 * * 2", "time_limit": 22}

        res = client.put(f"/1", json=data)

        assert res.status_code == 404
        assert res.json() == {"msg": f"Specified schedule 1 does not exist"}