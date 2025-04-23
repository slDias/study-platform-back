from sqlalchemy.orm import mapped_column, Mapped

from base import BaseModel


class Task(BaseModel):
    __tablename__ = "task"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.title:
            raise ValueError("title cannot be empty")
