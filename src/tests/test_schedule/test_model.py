import pytest
from sqlalchemy.exc import IntegrityError

from schedule import Schedule


def test_create_schedule(task_in_db):
    expected_cron = "0 0 * * 1"
    expected_time_limit = 24

    schedule = Schedule(
        cron=expected_cron, task=task_in_db, time_limit=expected_time_limit
    )

    assert schedule.id is None
    assert schedule.cron == expected_cron
    assert schedule.task == task_in_db
    assert schedule.task_id is None
    assert schedule.time_limit == expected_time_limit


async def test_save_schedule(task_in_db, session):
    expected_cron = "0 0 * * 1"
    expected_time_limit = 24
    schedule = Schedule(
        cron=expected_cron, task=task_in_db, time_limit=expected_time_limit
    )

    session.add(schedule)
    await session.commit()

    assert schedule.id is not None
    assert schedule.task_id == task_in_db.id


def test_schedule_must_have_a_task(task_in_db, session):
    with pytest.raises(ValueError):
        Schedule(cron="0 0 * * 1", task=None, time_limit=24)


async def test_schedules_task_can_be_an_id(task_in_db, session):
    s = Schedule(cron="0 0 * * 1", task_id=task_in_db.id, time_limit=24)

    session.add(s)
    await session.commit()

    assert s.id is not None
    assert s.task == task_in_db


async def test_schedules_task_must_exist(session):
    s = Schedule(cron="0 0 * * 1", task_id=999, time_limit=24)
    session.add(s)

    with pytest.raises(IntegrityError):
        await session.commit()

    assert s.id is None
    assert s.task is None
