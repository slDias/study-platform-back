from datetime import datetime, UTC

import pytest

from assignment import Assignment


@pytest.fixture
async def assignment_in_db(session, schedule_in_db):
    a = Assignment(task=schedule_in_db.task, scheduler=schedule_in_db, due_datetime=datetime.now(UTC))
    session.add(a)
    await session.commit()
    return a