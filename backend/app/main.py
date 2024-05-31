from fastapi import FastAPI
from fastapi.routing import APIRoute

from app.api.routers import api_router
from app.core.config import settings

def custom_generate_unique_id(route: APIRoute):
    return f"{route.tags[0]}-{route.name}"

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    generate_unique_id_function=custom_generate_unique_id,
)

# TODO: CORS configuration

app.include_router(api_router, prefix=settings.API_V1_STR)
