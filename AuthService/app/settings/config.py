from pydantic import Field, PostgresDsn
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    postgres_connection: PostgresDsn = Field(
        "postgresql+asyncpg://postgres:postgres@localhost:5432/postgres",
        alias="POSTGRES_CONNECTION",
        json_schema_extra={"env": "POSTGRES_CONNECTION"},
    )
    echo: bool = Field(
        False,
        alias="ECHO",
        json_schema_extra={"env": "ECHO"},
    )
    access_expiratioin_seconds: int = Field(
        1800,
        alias="ACCESS_EXPIRATION_SECONDS",
        json_schema_extra={"env": "ACCESS_EXPIRATION_SECONDS"},
    )
    refresh_expiratioin_seconds: int = Field(
        1800,
        alias="REFRESH_EXPIRATION_SECONDS",
        json_schema_extra={"env": "REFRESH_EXPIRATION_SECONDS"},
    )
    social_auth_redirect_url: str = Field(
        "http://localhost:8000/auth/redirect",
        alias="SOCIAL_AUTH_REDIRECT_URL",
        json_schema_extra={"env": "SOCIAL_AUTH_REDIRECT_URL"},
    )
    redis_host: str = Field(
        "localhost",
        alias="REDIS_HOST",
        json_schema_extra={"env": "REDIS_HOST"},
    )
    redis_password: str = Field(
        "password",
        alias="REDIS_PASSWORD",
        json_schema_extra={"env": "REDIS_PASSWORD"},
    )
    
settings = Settings()
