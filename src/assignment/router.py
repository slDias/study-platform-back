from fastapi import APIRouter
from sqlalchemy import select
from sqlalchemy.orm import joinedload

from assignment import Assignment
from assignment.schema import AssignmentSchema
from dependencies import SessionDep

assignment_router = APIRouter()


@assignment_router.get("/")
async def list_assignments(session: SessionDep):
    assignment_list = await session.scalars(
        select(Assignment)
        .options(
            joinedload(Assignment.task),
            joinedload(Assignment.scheduler)
        )
    )
    return [AssignmentSchema.model_validate(a) for a in assignment_list]
