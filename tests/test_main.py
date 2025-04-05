import pytest

from fastapi.testclient import TestClient

from main import app


def test_health_endpoint(client):

    res = client.get("/")

    assert res.status_code == 200
    assert res.json() == "OK"
