from fastapi import APIRouter

from app.api.routes import file, login, user

api_router = APIRouter()

api_router.include_router(login.router, tags=["login"])
api_router.include_router(file.router, prefix="/files", tags=["files"])
api_router.include_router(user.router, prefix="/users", tags=["users"])
