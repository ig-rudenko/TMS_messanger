from fastapi import FastAPI

from app.auth.handlers import router as auth_router
from app.friendship.handlers import router as friendship_router
from app.chats.handlers import router as chats_router

app = FastAPI()

app.include_router(chats_router, prefix='/api/v1')
app.include_router(auth_router, prefix='/api/v1')
app.include_router(friendship_router, prefix='/api/v1')
