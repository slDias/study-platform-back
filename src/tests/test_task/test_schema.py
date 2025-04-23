import random
import uuid

import pytest
from pydantic import ValidationError

from task import TaskSchema


def test_serialize_task():
    expected_id = random.randint(1, 10)
    expected_title = uuid.uuid4().hex
    task_data = {"id": expected_id, "title": expected_title}

    serialized_task = TaskSchema(**task_data)

    assert serialized_task.id == expected_id
    assert serialized_task.title == expected_title

def test_id_can_be_none():
    expected_title = uuid.uuid4().hex
    task_data = {"id": None, "title": expected_title}

    serialized_task = TaskSchema(**task_data)

    assert serialized_task.id is None
    assert serialized_task.title == expected_title

def test_id_can_be_omitted():
    expected_title = uuid.uuid4().hex
    task_data = {"title": expected_title}

    serialized_task = TaskSchema(**task_data)

    assert serialized_task.id is None
    assert serialized_task.title == expected_title

def test_title_cannot_be_none():
    task_data = {"id": 1, "title": None}

    with pytest.raises(ValidationError):
        TaskSchema(**task_data)

def test_title_cannot_be_omitted():
    task_data = {"id": 1}

    with pytest.raises(ValidationError):
        TaskSchema(**task_data)

def test_title_cannot_be_empty_str():
    task_data = {"id": 1, "title": ""}

    with pytest.raises(ValidationError):
        TaskSchema(**task_data)
