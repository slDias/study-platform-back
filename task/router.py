from fastapi import APIRouter
from sqlalchemy import select

from dependencies import SessionDep
from task.model import Task

task_router = APIRouter()

@task_router.get("/")
async def root(session: SessionDep):
    result = await session.execute(select(Task))
    res = [t for t in result.fetchall()]
    return res
