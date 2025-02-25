
from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    kafka_url: str = Field(
        "localhost:9092",
        alias="KAFKA_URL",
        json_schema_extra={"env": "KAFKA_URL"},
    )
    kafka_topic: str = Field(
        "telegram_bot",
        alias="KAFKA_TOPIC",
        json_schema_extra={"env": "KAFKA_TOPIC"}
    )
    kafka_group_id: str = Field(
        "telegram_bot",
        alias="KAFKA_GROUP_ID",
        json_schema_extra={"env": "KAFKA_GROUP_ID"}
    )
    
    tg_token: str = Field(
        "token",
        alias="TG_TOKEN",
        json_schema_extra={"env": "TG_TOKEN"}
    )
    chat_id: str = Field(
        "chat_id",
        alias="TG_CHAT_ID",
        json_schema_extra={"env": "TG_CHAT_ID"}
    )
    
settings = Settings()