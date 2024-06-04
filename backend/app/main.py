from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.routing import APIRoute

from app.api.routers import api_router
from app.cache.core import redis_db as redis
from app.core.config import settings

def custom_generate_unique_id(route: APIRoute):
    return f"{route.tags[0]}-{route.name}"

@asynccontextmanager
async def lifespan(app: FastAPI):
    redis.connect()

    yield

    redis.disconnect()

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    generate_unique_id_function=custom_generate_unique_id,
    lifespan=lifespan,
)

# TODO: CORS configuration

app.include_router(api_router, prefix=settings.API_V1_STR)
