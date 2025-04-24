from datetime import datetime, UTC, timedelta

from assignment import Assignment


def test_create_assignment(schedule_in_db):
    expected_date = datetime.now(UTC) + timedelta(days=1)

    assignment = Assignment(task=schedule_in_db.task, scheduler=schedule_in_db, due_date=expected_date)

    assert assignment.id is None
    assert assignment.task == schedule_in_db.task
    assert assignment.scheduler == schedule_in_db
    assert assignment.due_date == expected_date
    assert assignment.status is not None  # todo define status
