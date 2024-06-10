from datetime import timedelta
import secrets
from typing import Annotated, Any, Literal

from pydantic import (
    AnyUrl,
    BeforeValidator,
    PostgresDsn,
    computed_field,
)
from pydantic_core import MultiHostUrl
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import find_dotenv

def parse_cors(v: Any) -> list[str] | str:
    if isinstance(v, str) and not v.startswith("["):
        return [i.strip() for i in v.split(",")]
    elif isinstance(v, list | str):
        return v
    raise ValueError(v)

class Settings(BaseSettings):
    # Use environment variables from the global file
    model_config = SettingsConfigDict(
        env_file=find_dotenv(filename=".env"),
        env_ignore_empty=True,
        extra="ignore",
    )

    # App metadata config
    PROJECT_NAME: str = "fileshare"

    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)

    DOMAIN: str = "localhost"
    ENVIRONMENT: Literal["local", "staging", "production"] = "local"

    BACKEND_CORS_ORIGINS: Annotated[
        list[AnyUrl] | str, BeforeValidator(parse_cors)
    ] = []

    USERS_OPEN_REGISTRATION: bool = True

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7 # 7 days

    # Database Config
    POSTGRES_SERVER: str
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str = ""

    @computed_field
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> PostgresDsn:
        return MultiHostUrl.build(
            scheme="postgresql+psycopg",
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_SERVER,
            port=self.POSTGRES_PORT,
            path=self.POSTGRES_DB,
        )

    # Testing Database Config
    SQLALCHEMY_TESTING_DATABASE_URI: str = "sqlite://"
    TEST_USER_EMAIL: str = "user@email.com"
    TEST_USER_PASSWORD: str = "password"

    # Cache Config
    REDIS_SERVER: str
    REDIS_PORT: int = 6379
    REDIS_PASSWORD: str | None = ""
    REDIS_DB: int = 0

    REDIS_CACHE_EXPIRY: timedelta = timedelta(seconds=3600)


settings = Settings() # type: ignore
