import pytest
from fastapi import APIRouter

from fastapi.testclient import TestClient

from main import app
from task.router import task_router


def test_health_endpoint(client):

    res = client.get("/")

    assert res.status_code == 200
    assert res.json() == "OK"


def test_has_task_router():
    expected_router = APIRouter()
    expected_router.include_router(task_router, prefix="/task")
    assert all(task_route in app.routes for task_route in expected_router.routes)
