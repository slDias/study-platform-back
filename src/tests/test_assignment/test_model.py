from datetime import UTC, datetime, timedelta

import pytest
from sqlalchemy.exc import IntegrityError

from assignment import Assignment


def test_create_assignment(schedule_in_db):
    expected_date = datetime.now(UTC) + timedelta(days=1)

    assignment = Assignment(
        task=schedule_in_db.task, scheduler=schedule_in_db, due_datetime=expected_date
    )

    assert assignment.id is None
    assert assignment.task == schedule_in_db.task
    assert assignment.scheduler == schedule_in_db
    assert assignment.due_datetime == expected_date
    assert assignment.submission_datetime is None


async def test_save_assignment(session, schedule_in_db):
    assignment = Assignment(
        task=schedule_in_db.task,
        scheduler=schedule_in_db,
        due_datetime=datetime.now(UTC),
    )
    session.add(assignment)

    await session.commit()

    assert assignment.id is not None


def test_task_is_required(schedule_in_db):
    with pytest.raises(ValueError):
        Assignment(task=None, scheduler=schedule_in_db, due_datetime=datetime.now(UTC))


async def test_task_must_exist(session, schedule_in_db):
    a = Assignment(
        task_id=999, scheduler=schedule_in_db, due_datetime=datetime.now(UTC)
    )
    session.add(a)

    with pytest.raises(IntegrityError):
        await session.commit()

    assert a.id is None
    assert a.task is None


def test_scheduler_can_be_none(task_in_db):
    a = Assignment(task=task_in_db, scheduler=None, due_datetime=datetime.now(UTC))

    assert a.id is None
    assert a.scheduler is None


def test_scheduler_is_optional(task_in_db):
    a = Assignment(task=task_in_db, due_datetime=datetime.now(UTC))

    assert a.id is None
    assert a.scheduler is None


async def test_scheduler_must_exist_if_specified(task_in_db, session):
    a = Assignment(task=task_in_db, scheduler_id=999, due_datetime=datetime.now(UTC))
    session.add(a)

    with pytest.raises(IntegrityError):
        await session.commit()

    assert a.id is None
    assert a.scheduler is None


def test_due_datetime_can_be_iso_string(schedule_in_db):
    expected_date = datetime.now(UTC) + timedelta(days=1)
    expected_date_str = expected_date.isoformat()

    assignment = Assignment(
        task=schedule_in_db.task,
        scheduler=schedule_in_db,
        due_datetime=expected_date_str,
    )

    assert assignment.id is None
    assert assignment.due_datetime == expected_date


def test_due_datetime_iso_string_must_be_valid(schedule_in_db):
    with pytest.raises(ValueError):
        Assignment(
            task=schedule_in_db.task, scheduler=schedule_in_db, due_datetime="aaaaaaa"
        )


def test_due_datetime_must_be_utc(schedule_in_db):
    with pytest.raises(ValueError):
        Assignment(
            task=schedule_in_db.task,
            scheduler=schedule_in_db,
            due_datetime=datetime.now(),
        )


def test_submission_date_can_be_iso_string(schedule_in_db):
    expected_date = datetime.now(UTC) + timedelta(days=1)
    expected_date_str = expected_date.isoformat()

    assignment = Assignment(
        task=schedule_in_db.task,
        scheduler=schedule_in_db,
        due_datetime=datetime.now(UTC),
        submission_datetime=expected_date_str,
    )

    assert assignment.id is None
    assert assignment.submission_datetime == expected_date


def test_submission_date_iso_string_must_be_valid(schedule_in_db):
    with pytest.raises(ValueError):
        Assignment(
            task=schedule_in_db.task,
            scheduler=schedule_in_db,
            due_datetime=datetime.now(UTC),
            submission_datetime="aaaaaaaaaaa",
        )


def test_submission_date_must_be_utc(schedule_in_db):
    with pytest.raises(ValueError):
        Assignment(
            task=schedule_in_db.task,
            scheduler=schedule_in_db,
            due_datetime=datetime.now(UTC),
            submission_datetime=datetime.now(),
        )
