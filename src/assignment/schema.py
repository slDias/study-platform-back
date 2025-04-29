from datetime import datetime
from typing import Self

from pydantic import model_validator

from base import BaseSchema
from schedule import ScheduleSchema
from task import TaskSchema


class AssignmentSchema(BaseSchema):
    id: int | None = None
    task: TaskSchema | None = None
    task_id: int | None = None
    scheduler: ScheduleSchema | None = None
    scheduler_id: int | None = None
    due_datetime: datetime
    submission_datetime: datetime | None = None

    @model_validator(mode='after')
    def _validate(self) -> Self:
        self._check_has_a_task()
        return self

    def _check_has_a_task(self) -> None:
        if self.task is None and self.task_id is None:
            raise ValueError('Schedule has no Task')

        if not self.task_id:
            self.task_id = self.task.id

        if self.task_id and self.task and self.task_id != self.task.id:
            raise ValueError(f'Specified task {self.task.id} and task id {self.task_id} does not match')
