from fastapi import APIRouter
from sqlalchemy import select
from starlette import status
from starlette.responses import Response

from dependencies import SessionDep
from schedule import ScheduleSchema, Schedule

schedule_router = APIRouter()

@schedule_router.get("/")
async def list_schedules(session: SessionDep):
    result = await session.scalars(select(Schedule))
    return [ScheduleSchema.model_validate(s) for s in result]


@schedule_router.get("/{schedule_id}")
async def get_single_schedule(schedule_id: int, session: SessionDep, response: Response):
    result = await session.get(Schedule, schedule_id)

    if not result:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"msg": f"No schedule with id {schedule_id}"}

    return ScheduleSchema.model_validate(result)


@schedule_router.post("/")
async def create_schedule(schedule_data: ScheduleSchema, session: SessionDep):
    schedule = Schedule(**schedule_data.model_dump(exclude_none=True))
    session.add(schedule)
    await session.commit()
    return ScheduleSchema.model_validate(schedule)
