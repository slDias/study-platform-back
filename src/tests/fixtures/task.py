import uuid

import pytest

from task import Task


@pytest.fixture
async def task_in_db(session):
    task = Task(title=uuid.uuid4().hex)
    session.add(task)
    await session.commit()
    return task