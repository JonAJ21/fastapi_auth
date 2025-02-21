from pydantic import Field, PostgresDsn
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    postgres_connection: PostgresDsn = Field(
        "postgresql+asyncpg://postgres:postgres@localhost:5432/postgres",
        alias="POSTGRES_CONNECTION",
        env="POSTGRES_CONNECTION",
    )
    echo: bool = Field(
        False,
        alias="ECHO",
        env="ECHO",
    )
    access_expiratioin_seconds: int = Field(
        1800,
        alias="ACCESS_EXPIRATION_SECONDS",
        env="ACCESS_EXPIRATION_SECONDS",
    )
    
settings = Settings()