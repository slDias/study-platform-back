from typing import Self

from pydantic import Field, model_validator
from croniter import croniter

from base import BaseSchema
from task import TaskSchema, Task


class ScheduleSchema(BaseSchema):
    id: int | None = None
    task: TaskSchema | None = Field(default=None)
    task_id: int | None = None
    cron: str
    time_limit: int = Field(gt=0)

    @model_validator(mode='after')
    def _validate(self):
        self._check_has_a_task()
        self._check_cron_is_valid()
        return self

    def _check_has_a_task(self) -> Self:
        if self.task is None and self.task_id is None:
            raise ValueError('Schedule has no Task')

    def _check_cron_is_valid(self) -> Self:
        try:
            croniter(self.cron)
        except:
            raise ValueError('cron is not a valid crontab')
