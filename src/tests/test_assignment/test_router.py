import pytest
from starlette.testclient import TestClient

from assignment.router import assignment_router


@pytest.fixture
def client(empty_app):
    empty_app.include_router(assignment_router)
    return TestClient(empty_app)


class TestGet:

    async def test_list_all(self, client, assignment_in_db):
        res = client.get("/")

        data = res.json()
        assert len(data) == 1
        assert data[0]["id"] == assignment_in_db.id

