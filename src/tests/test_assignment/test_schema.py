import random
from datetime import datetime, UTC, timedelta

import pytest
from pydantic import ValidationError

from assignment.schema import AssignmentSchema


@pytest.fixture
def task_data(schedule_in_db):
    return {"id": schedule_in_db.task_id, "title": schedule_in_db.task.title}

@pytest.fixture
def schedule_data(schedule_in_db, task_data):
    return {"id": schedule_in_db.id, "task": task_data, "cron": "0 0 * * 1", "time_limit": 24}

@pytest.fixture
def assignment_data(schedule_data, task_data):
    return {"id": random.randint(1, 10), "task": task_data, "scheduler": schedule_data,
            "due_datetime": datetime.now(UTC), "submission_datetime": datetime.now(UTC)}


def test_parse_schema(task_data, schedule_data, schedule_in_db):
    expected_id = random.randint(1, 10)
    expected_due_datetime = datetime.now(UTC)
    expected_sub_datetime = datetime.now(UTC) + timedelta(hours=1)

    a = AssignmentSchema(**{
        "id": expected_id,
        "task": task_data,
        "scheduler": schedule_data,
        "due_datetime": expected_due_datetime.isoformat(),
        "submission_datetime": expected_sub_datetime.isoformat()
    })

    assert a.id == expected_id
    assert a.task.id == schedule_in_db.task.id
    assert a.task.title == schedule_in_db.task.title
    assert a.scheduler.id == schedule_in_db.id
    assert a.scheduler.task_id == schedule_in_db.task_id
    assert a.scheduler.cron == schedule_in_db.cron
    assert a.scheduler.time_limit == schedule_in_db.time_limit
    assert a.due_datetime == expected_due_datetime
    assert a.submission_datetime == expected_sub_datetime


def test_id_can_be_ommitted(assignment_data):
    del assignment_data["id"]

    a = AssignmentSchema(**assignment_data)

    assert a.id is None

def test_id_can_be_none(assignment_data):
    del assignment_data["id"]
    assignment_data["id"] = None

    a = AssignmentSchema(**assignment_data)

    assert a.id is None
    
def test_task_is_required(assignment_data):
    del assignment_data["task"]

    with pytest.raises(ValidationError):
        AssignmentSchema(**assignment_data)

def test_task_can_be_id(assignment_data, schedule_in_db):
    assignment_data["task_id"] = schedule_in_db.task_id
    del assignment_data["task"]

    a = AssignmentSchema(**assignment_data)

    assert a.task_id == schedule_in_db.task_id
    assert a.task is None


def test_scheduler_is_optional(assignment_data):
    del assignment_data["scheduler"]

    a = AssignmentSchema(**assignment_data)

    assert a.scheduler is None

def test_scheduler_can_be_id(assignment_data, schedule_in_db):
    assignment_data["scheduler_id"] = schedule_in_db.id
    del assignment_data["scheduler"]

    a = AssignmentSchema(**assignment_data)

    assert a.scheduler_id == schedule_in_db.id
    assert a.scheduler is None

def test_due_datetime_is_required(assignment_data):
    del assignment_data["due_datetime"]

    with pytest.raises(ValidationError):
        AssignmentSchema(**assignment_data)

def test_due_datetime_must_be_valid_iso(assignment_data):
    assignment_data["due_datetime"] = "aaaa"

    with pytest.raises(ValidationError):
        AssignmentSchema(**assignment_data)

def test_submission_datetime_must_be_valid_iso(assignment_data):
    assignment_data["submission_datetime"] = "aaaa"

    with pytest.raises(ValidationError):
        AssignmentSchema(**assignment_data)

def test_submission_datetime_is_optional(assignment_data):
    del assignment_data["submission_datetime"]

    a = AssignmentSchema(**assignment_data)

    assert a.submission_datetime is None
