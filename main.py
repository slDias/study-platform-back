from fastapi import FastAPI

from dependencies import lifespan

app = FastAPI(lifespan=lifespan)

@app.get("/")
async def health():
    return "OK"
