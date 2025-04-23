from fastapi import APIRouter, Response, status
from sqlalchemy import select, update

from dependencies import SessionDep
from task.model import Task
from task.schema import TaskSchema

task_router = APIRouter()

@task_router.get("/")
async def list_tasks(session: SessionDep):
    result = await session.scalars(select(Task))
    return [TaskSchema.model_validate(t) for t in result]

@task_router.get("/{task_id}")
async def get_single_task(task_id: int, session: SessionDep, response: Response):
    task = await session.get(Task, task_id)

    if not task:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"msg": f"No task with id {task_id}"}

    return task

@task_router.post("/")
async def create_task(task_data: TaskSchema, session: SessionDep):
    task = Task(**task_data.model_dump())
    session.add(task)
    await session.commit()
    return TaskSchema.model_validate(task)

@task_router.put("/{task_id}")
async def update_task(task_id: int, task_data: TaskSchema, session: SessionDep, response: Response):
    task = await session.scalar(
        update(Task).where(Task.id == task_id).values(**task_data.model_dump(exclude_unset=True)).returning(Task)
    )

    await session.commit()

    if not task:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"msg": f"No task with id {task_id}"}

    return TaskSchema.model_validate(task)
