from typing import Self

from croniter import croniter
from pydantic import Field, model_validator

from base import BaseSchema
from task import TaskSchema


class ScheduleSchema(BaseSchema):
    id: int | None = None
    task: TaskSchema | None = Field(default=None)
    task_id: int | None = None
    cron: str
    time_limit: int = Field(gt=0)

    @model_validator(mode="after")
    def _validate(self):
        self._check_has_a_task()
        self._check_cron_is_valid()
        return self

    def _check_has_a_task(self) -> Self:
        if self.task is None and self.task_id is None:
            raise ValueError("Schedule has no Task")

        if not self.task_id and self.task is not None:
            self.task_id = self.task.id

        if self.task_id and self.task and self.task_id != self.task.id:
            raise ValueError(
                f"Specified task {self.task.id} and task id {self.task_id} does not match"
            )

        return self

    def _check_cron_is_valid(self) -> Self:
        try:
            croniter(self.cron)
        except Exception as e:
            raise ValueError("cron is not a valid crontab") from e

        return self
