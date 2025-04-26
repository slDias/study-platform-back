from datetime import datetime, UTC, timedelta

import pytest
from sqlalchemy.exc import IntegrityError

from assignment import Assignment


def test_create_assignment(schedule_in_db):
    expected_date = datetime.now(UTC) + timedelta(days=1)

    assignment = Assignment(task=schedule_in_db.task, scheduler=schedule_in_db, due_datetime=expected_date)

    assert assignment.id is None
    assert assignment.task == schedule_in_db.task
    assert assignment.scheduler == schedule_in_db
    assert assignment.due_datetime == expected_date
    assert assignment.submission_datetime is None


async def test_save_assignment(session, schedule_in_db):
    assignment = Assignment(
        task=schedule_in_db.task,
        scheduler=schedule_in_db,
        due_datetime=datetime.now(UTC)
    )
    session.add(assignment)

    await session.commit()

    assert assignment.id is not None

def test_task_is_required(schedule_in_db):
    with pytest.raises(ValueError):
        Assignment(task=None, scheduler=schedule_in_db, due_datetime=datetime.now(UTC))

async def test_task_must_exist(session, schedule_in_db):
    a = Assignment(task_id=999, scheduler=schedule_in_db, due_datetime=datetime.now(UTC))
    session.add(a)

    with pytest.raises(IntegrityError):
        await session.commit()

    assert a.id is None
    assert a.task is None

def test_scheduler_can_be_none(task_in_db):  # todo
    assert False

def test_scheduler_must_exist_if_specified():
    assert False

def test_due_datetime_must_be_valid(schedule_in_db):
    assert False

def test_due_datetime_must_be_utc(schedule_in_db):
    assert False

def test_submission_date_must_be_valid(schedule_in_db):
    assert False

def test_submission_date_must_be_utc(schedule_in_db):
    assert False
