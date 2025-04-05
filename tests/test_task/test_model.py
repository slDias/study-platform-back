import pytest

from task.model import Task


def test_create_task():
    expected_title = "Task title"

    task = Task(title=expected_title)

    assert task.id is None
    assert task.title == expected_title

async def test_save_task(session):
    expected_title = "Task title"
    task = Task(title=expected_title)
    session.add(task)

    await session.commit()

    assert task.id is not None
    assert task.title == expected_title
