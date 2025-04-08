from sqlalchemy.orm import MappedColumn, mapped_column

from base import BaseModel


class Task(BaseModel):
    __tablename__ = "task"

    id: MappedColumn[int] = mapped_column(primary_key=True)
    title: MappedColumn[str | None]
