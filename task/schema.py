from pydantic import Field

from base import BaseSchema


class TaskSchema(BaseSchema):
    id: int | None = None
    title: str = Field(min_length=1)
