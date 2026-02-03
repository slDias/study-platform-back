from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from base import BaseModel
from task import Task


class Schedule(BaseModel):
    __tablename__ = "schedule"

    id: Mapped[int] = mapped_column(primary_key=True)
    task_id: Mapped[int] = mapped_column(ForeignKey("task.id"))
    task: Mapped["Task"] = relationship()
    cron: Mapped[str]
    time_limit: Mapped[int]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if not self.task and not self.task_id:
            raise ValueError("Schedule must have an associated task")
