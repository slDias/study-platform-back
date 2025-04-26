from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from base import BaseModel


class Assignment(BaseModel):
    __tablename__ = "assignment"

    id: Mapped[int] = mapped_column(primary_key=True)
    task: Mapped['Task'] = relationship()
    task_id: Mapped[int] = mapped_column(ForeignKey("task.id"))
    scheduler: Mapped['Schedule'] = relationship()
    scheduler_id: Mapped[int] = mapped_column(ForeignKey("schedule.id"))
    due_datetime: Mapped[datetime]
    submission_datetime: Mapped[datetime | None]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if not self.task and not self.task_id:
            raise ValueError("Schedule must have an associated task")
