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
    due_date: Mapped[datetime]
    status: Mapped[str] = "Something"  # todo
