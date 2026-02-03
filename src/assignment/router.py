from datetime import UTC, datetime

from fastapi import APIRouter
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from starlette import status
from starlette.responses import Response

from dependencies import SessionDep

from .model import Assignment
from .schema import AssignmentSchema

assignment_router = APIRouter()


@assignment_router.get("/")
async def list_assignments(session: SessionDep, show_expired: bool = False):
    query = select(Assignment).options(
        joinedload(Assignment.task), joinedload(Assignment.scheduler)
    )

    if show_expired is False:
        query = query.where(Assignment.due_datetime > datetime.now(UTC))

    assignment_list = await session.scalars(query)
    result = [AssignmentSchema.model_validate(a) for a in assignment_list]
    return result


@assignment_router.post("/{assignment_id}/submit")
async def submit_assignment(
    session: SessionDep, assignment_id: int, response: Response
):
    assignment = await session.get(Assignment, assignment_id)

    if assignment is None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"msg": f"No assignment with id {assignment_id}"}

    assignment.submission_datetime = datetime.now(UTC)
    await session.commit()
    return assignment.submission_datetime
