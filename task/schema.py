from pydantic import BaseModel

from task.model import Task


class TaskSchema(BaseModel):
    id: int | None = None
    title: str

    @classmethod
    def from_model(cls, task: Task):
        return cls(id=task.id, title=task.title)
