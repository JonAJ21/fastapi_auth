from pydantic import Field, PostgresDsn
from pydantic_settings import BaseSettings

class TestSettings(BaseSettings):
    postgres_connection: PostgresDsn = Field(
        "postgresql+asyncpg://postgres:postgres@localhost:5432/postgres",
        alias="TEST_POSTGRES_CONNECTION",
        json_schema_extra={"env": "TEST_POSTGRES_CONNECTION"},
    )
    echo: bool = Field(
        False,
        alias="ECHO",
        json_schema_extra={"env": "ECHO"},
    )
    redis_host: str = Field(
        "localhost",
        alias="TEST_REDIS_HOST",
        json_schema_extra={"env": "TEST_REDIS_HOST"},
    )
    redis_password: str = Field(
        "password",
        alias="TEST_REDIS_PASSWORD",
        json_schema_extra={"env": "TEST_REDIS_PASSWORD"},
    )
    
settings = TestSettings()