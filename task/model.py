from sqlalchemy.orm import MappedColumn, mapped_column, validates

from base import BaseModel


class Task(BaseModel):
    __tablename__ = "task"

    id: MappedColumn[int] = mapped_column(primary_key=True)
    title: MappedColumn[str]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.title:
            raise ValueError("title cannot be empty")
