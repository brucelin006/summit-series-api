from fastapi import FastAPI
from .player.router import router as player_router

app = FastAPI()

app.include_router(player_router)


@app.get("/")
async def root():
    return "Server is running..."
