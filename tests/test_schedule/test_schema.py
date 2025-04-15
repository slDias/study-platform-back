import random
import uuid

import pytest
from pydantic import ValidationError

from schedule import ScheduleSchema
from task import TaskSchema, Task


@pytest.fixture
def task_data():
    return {"id": 2, "title": uuid.uuid4().hex}


@pytest.fixture
def good_data(task_data):
    return {
        "id": random.randint(1, 10),
        "task": task_data,
        "cron": "0 0 * * 1",
        "time_limit": 24
    }


def test_serialize_schedule(task_data):
    expected_id = 1
    expected_cron = "0 0 * * 1"
    expected_time_limit = 24
    schedule_data = {
        "id": expected_id,
        "task": task_data,
        "cron": expected_cron,
        "time_limit": expected_time_limit
    }

    schedule = ScheduleSchema(**schedule_data)

    assert schedule.id == expected_id
    assert isinstance(schedule.task, TaskSchema)
    assert schedule.cron == expected_cron
    assert schedule.time_limit == expected_time_limit
    assert schedule.task_id == schedule.task.id


def test_id_can_be_none(good_data):
    data = good_data
    data["id"] = None

    schedule = ScheduleSchema(**data)

    assert schedule.id is None


def test_id_can_be_omitted(good_data):
    data = good_data
    del data["id"]

    schedule = ScheduleSchema(**data)

    assert schedule.id is None


def test_task_can_be_an_id(good_data):
    data = good_data
    expected_id = random.randint(1, 10)
    del data["task"]
    data["task_id"] = expected_id

    schedule = ScheduleSchema(**data)

    assert schedule.task_id == expected_id

def test_task_id_must_be_equal_to_specified_task_if_present(good_data):
    data = good_data
    data["task_id"] = data["task"]["id"] + 1

    with pytest.raises(ValidationError):
        ScheduleSchema(**data)


def test_must_have_a_task(good_data):
    data = good_data
    del good_data["task"]

    with pytest.raises(ValueError):
        ScheduleSchema(**data)


def test_cron_is_required(good_data):
    data = good_data
    del data["cron"]

    with pytest.raises(ValidationError):
        ScheduleSchema(**data)


def test_cron_must_be_valid_format(good_data):
    data = good_data
    data["cron"] = "abc"

    with pytest.raises(ValidationError):
        ScheduleSchema(**data)


def test_time_limit_is_required(good_data):
    data = good_data
    del data["time_limit"]

    with pytest.raises(ValidationError):
        ScheduleSchema(**data)


def test_time_limit_must_be_positive(good_data):
    data = good_data
    data["time_limit"] = -1

    with pytest.raises(ValidationError):
        ScheduleSchema(**data)