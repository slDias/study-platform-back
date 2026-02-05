from fastapi import APIRouter
from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload
from starlette import status
from starlette.responses import Response

from dependencies import SessionDep

from .model import Schedule
from .schema import ScheduleSchema

schedule_router = APIRouter()


@schedule_router.get("/")
async def list_schedules(session: SessionDep):
    result = await session.scalars(
        select(Schedule).options(joinedload(Schedule.task))
    )
    return [ScheduleSchema.model_validate(s) for s in result]


@schedule_router.get("/{schedule_id}")
async def get_single_schedule(
    schedule_id: int, session: SessionDep, response: Response
):
    result = await session.scalar(
        select(Schedule)
        .options(joinedload(Schedule.task))
        .filter(Schedule.id == schedule_id)
    )

    if not result:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"msg": f"No schedule with id {schedule_id}"}

    return ScheduleSchema.model_validate(result)


@schedule_router.post("/")
async def create_schedule(
    schedule_data: ScheduleSchema, session: SessionDep, response: Response
):
    schedule = Schedule(
        **schedule_data.model_dump(exclude_none=True, exclude={"task"})
    )
    session.add(schedule)

    try:
        await session.commit()
    except IntegrityError:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"msg": f"Specified task {schedule_data.task_id} does not exist"}

    await session.refresh(schedule, attribute_names=("task",))

    return ScheduleSchema.model_validate(schedule)


@schedule_router.put("/{schedule_id}")
async def update_schedule(
    schedule_id: int,
    schedule_data: ScheduleSchema,
    session: SessionDep,
    response: Response,
):
    try:
        schedule = await session.scalar(
            update(Schedule)
            .where(Schedule.id == schedule_id)
            .values(
                **schedule_data.model_dump(exclude_unset=True, exclude={"task"})
            )
            .returning(Schedule)
        )

        if not schedule:
            response.status_code = status.HTTP_404_NOT_FOUND
            return {"msg": f"Specified schedule {schedule_id} does not exist"}

    except IntegrityError:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"msg": f"Specified task {schedule_data.task_id} does not exist"}

    await session.commit()
    await session.refresh(schedule, attribute_names=("task",))

    return ScheduleSchema.model_validate(schedule)
