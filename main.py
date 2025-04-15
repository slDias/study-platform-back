from fastapi import FastAPI

from dependencies import lifespan
from schedule import schedule_router
from task.router import task_router

app = FastAPI(lifespan=lifespan)
app.include_router(task_router, prefix="/task")
app.include_router(schedule_router, prefix="/schedule")

@app.get("/")
async def health():
    return "OK"


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
