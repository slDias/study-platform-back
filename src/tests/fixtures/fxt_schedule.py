import pytest

from schedule import Schedule


@pytest.fixture
async def schedule_in_db(session, task_in_db):
    s = Schedule(task=task_in_db, cron="0 0 * * 1", time_limit=24)
    session.add(s)
    await session.commit()
    return s