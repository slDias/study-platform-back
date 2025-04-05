from sqlalchemy.orm import MappedColumn, mapped_column

from models import Base


class Task(Base):
    __tablename__ = "task"

    id: MappedColumn[int] = mapped_column(primary_key=True)
    title: MappedColumn[str | None]


    def to_dict(self):
        return {"id": self.id, "title": self.title}
