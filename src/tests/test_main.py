from fastapi import APIRouter

from assignment import assignment_router
from main import app
from schedule import schedule_router
from task import task_router


def test_health_endpoint(client):
    res = client.get("/")

    assert res.status_code == 200
    assert res.json() == "OK"


def test_has_task_router():
    expected_router = APIRouter()
    expected_router.include_router(task_router, prefix="/task")

    assert all(task_route in app.routes for task_route in expected_router.routes)


def test_has_schedule_router():
    expected_router = APIRouter()
    expected_router.include_router(schedule_router, prefix="/schedule")

    assert all(task_route in app.routes for task_route in expected_router.routes)


def test_has_assignment_router():
    expected_router = APIRouter()
    expected_router.include_router(assignment_router, prefix="/assignment")

    assert all(route in app.routes for route in expected_router.routes)
