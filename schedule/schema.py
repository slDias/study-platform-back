from typing import Self

from pydantic import Field, model_validator

from base import BaseSchema
from task import TaskSchema, Task


class ScheduleSchema(BaseSchema):
    id: int | None = None
    task: TaskSchema | None = None
    task_id: int | None = None
    cron: str
    time_limit: int = Field(gt=0)

    @model_validator(mode='after')
    def check_passwords_match(self) -> Self:
        if self.task is None and self.task_id is None:
            raise ValueError('Schedule has no Task')
