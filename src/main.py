from fastapi import FastAPI

from dependencies import lifespan
from schedule import schedule_router
from task import task_router
from assignment import assignment_router

app = FastAPI(lifespan=lifespan)
app.include_router(task_router, prefix="/task")
app.include_router(schedule_router, prefix="/schedule")
app.include_router(assignment_router, prefix="/assignment")

@app.get("/")
async def health():
    return "OK"


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
