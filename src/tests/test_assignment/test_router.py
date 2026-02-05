from datetime import UTC, datetime, timedelta

import pytest
from sqlalchemy.ext.asyncio.session import close_all_sessions
from starlette.testclient import TestClient

from assignment import Assignment
from assignment.router import assignment_router


@pytest.fixture
def client(empty_app):
    empty_app.include_router(assignment_router)
    return TestClient(empty_app)


@pytest.fixture
async def expired_assignment(session, schedule_in_db):
    due_dt = datetime.now(UTC) - timedelta(hours=5)
    a = Assignment(
        task=schedule_in_db.task, scheduler=schedule_in_db, due_datetime=due_dt
    )
    session.add(a)
    await session.commit()
    return a


class TestGet:
    def test_list_non_expired(
        self, client, assignment_in_db, expired_assignment
    ):
        res = client.get("/")

        assert res.status_code == 200
        data = res.json()
        assert len(data) == 1
        assert data[0]["id"] == assignment_in_db.id

    def test_list_all(self, client, assignment_in_db, expired_assignment):
        res = client.get("/", params={"show_expired": True})

        assert res.status_code == 200
        data = res.json()
        assert len(data) == 2
        assert data[0]["id"] == assignment_in_db.id


class TestPost:
    async def test_set_as_done(self, client, session, assignment_in_db):
        res = client.post(f"/{assignment_in_db.id}/submit")

        assert res.status_code == 200
        await close_all_sessions()
        updated_assignment = await session.get(Assignment, assignment_in_db.id)
        assert updated_assignment.submission_datetime is not None

    def test_assignment_does_not_exists(self, client):
        res = client.post("/9999/submit")

        assert res.status_code == 404
