from datetime import datetime, UTC, timedelta

import pytest

from assignment import Assignment


@pytest.fixture
async def assignment_in_db(session, schedule_in_db):
    due_dt = datetime.now(UTC) + timedelta(hours=schedule_in_db.time_limit)
    a = Assignment(task=schedule_in_db.task, scheduler=schedule_in_db, due_datetime=due_dt)
    session.add(a)
    await session.commit()
    return a