import uuid

import pytest
from sqlalchemy.exc import IntegrityError

from schedule import Schedule
from task import Task
from tests.conftest import session


@pytest.fixture
async def task(session):
    t = Task(title=uuid.uuid4().hex)
    session.add(t)
    await session.commit()
    return t

def test_create_schedule(task):
    expected_cron = "0 0 * * 1"
    expected_time_limit = 24

    schedule = Schedule(cron=expected_cron, task=task, time_limit=expected_time_limit)

    assert schedule.id is None
    assert schedule.cron == expected_cron
    assert schedule.task == task
    assert schedule.task_id is None
    assert schedule.time_limit == expected_time_limit

async def test_save_schedule(task, session):
    expected_cron = "0 0 * * 1"
    expected_time_limit = 24
    schedule = Schedule(cron=expected_cron, task=task, time_limit=expected_time_limit)

    session.add(schedule)
    await session.commit()

    assert schedule.id is not None
    assert schedule.task_id == task.id


def test_schedule_must_have_a_task(task, session):
    with pytest.raises(ValueError):
        Schedule(cron="0 0 * * 1", task=None, time_limit=24)

async def test_schedules_task_can_be_an_id(task, session):
    s = Schedule(cron="0 0 * * 1", task_id=task.id, time_limit=24)

    session.add(s)
    await session.commit()

    assert s.id is not None
    assert s.task == task


async def test_schedules_task_must_exist(session):
    s = Schedule(cron="0 0 * * 1", task_id=999, time_limit=24)
    session.add(s)

    with pytest.raises(IntegrityError):
        await session.commit()
        assert s.id is not None
        assert s.task_id is None
