import pytest

from task import Task


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


def test_title_cannot_be_empty():
    with pytest.raises(ValueError):
        Task(title="")


def test_title_cannot_be_none():
    with pytest.raises(ValueError):
        Task(title=None)


def test_title_cannot_be_omitted():
    with pytest.raises(ValueError):
        Task()


async def test_id_cannot_be_duplicate(session):
    expected_title = "Task title"
    task = Task(title=expected_title)
    session.add(task)

    await session.commit()

    assert task.id is not None
    assert task.title == expected_title
