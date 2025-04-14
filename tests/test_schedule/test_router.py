import pytest
from sqlalchemy import select
from starlette.testclient import TestClient

from schedule import schedule_router, Schedule


@pytest.fixture
def client(empty_app):
    empty_app.include_router(schedule_router)
    return TestClient(empty_app)

@pytest.fixture
async def schedule_in_db(session, task_in_db):
    s = Schedule(task=task_in_db, cron="0 0 * * 1", time_limit=24)
    session.add(s)
    await session.commit()
    return s


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
    async def test_create_schedule(self, session, client, task_in_db):
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
