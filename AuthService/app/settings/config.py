from pydantic import EmailStr, Field, PostgresDsn
from pydantic_settings import BaseSettings
from async_fastapi_jwt_auth import AuthJWT

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
    base_dir: str = Field(
        "/app",
        alias="BASE_DIR",
        json_schema_extra={"env": "BASE_DIR"},
    )
    authjwt_secret_key: str = Field(
        "secret",
        alias="AUTHJWT_SECRET_KEY",
        json_schema_extra={"env": "AUTHJWT_SECRET_KEY"},
    )
    authjwt_denylist_enabled: bool = False
    authjwt_denylist_token_checks: set = {"access", "refresh"}
    authjwt_access_token_expires: int = Field(
        3600, 
        alias="JWT_ACCESS_EXP_TIME", 
        json_schema_extra={"env": "JWT_ACCESS_EXP_TIME"}
    )  # 2 minutes
    authjwt_refresh_token_expires: int = Field(
        3600, 
        alias="JWT_REFRESH_EXP_TIME", 
        json_schema_extra={"env": "JWT_REFRESH_EXP_TIME"}
    )  # 5 minutes
    authjwt_token_location: set = {"cookies", "headers"}
    authjwt_cookie_csrf_protect: bool = False
    authjwt_cookie_same_site: str = "lax"
    
    
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
    rate_limit_requests_per_interval: int = Field(
        1,
        alias="RATE_LIMIT_REQUESTS_PER_INTERVAL",
        json_schema_extra={"env": "RATE_LIMIT_REQUESTS_PER_INTERVAL"},
    )
    requests_interval: int = Field(
        1,
        alias="REQUESTS_INTERVAL",
        json_schema_extra={"env": "REQUESTS_INTERVAL"},
    )
    kafka_url: str = Field(
        "kafka:29092",
        alias="KAFKA_URL",
        json_schema_extra={"env": "KAFKA_URL"},
    )
    
    yandex_client_id: str = Field(
        "<client_id>",
        alias="YANDEX_CLIENT_ID",
        json_schema_extra={"env": "YANDEX_CLIENT_ID"},
    )
    yandex_client_secret: str = Field(
        "<client_secret>",
        alias="YANDEX_CLIENT_SECRET",
        json_schema_extra={"env": "YANDEX_CLIENT_SECRET"},
    )
    yandex_auth_base_url: str = Field(
        "https://oauth.yandex.ru/authorize",
        alias="YANDEX_AUTH_BASE_URL",
        json_schema_extra={"env": "YANDEX_AUTH_BASE_URL"},
    )
    yandex_auth_token_url: str = Field(
        "https://oauth.yandex.ru/token",
        alias="YANDEX_AUTH_TOKEN_URL",
        json_schema_extra={"env": "YANDEX_AUTH_TOKEN_URL"},
    )
    yandex_userinfo_url: str = Field(
        "https://login.yandex.ru/info",
        alias="YANDEX_USERINFO_URL",
        json_schema_extra={"env": "YANDEX_USERINFO_URL"},
    )
    
    
    
    vk_client_id: str = Field(
        "<client_id>",
        alias="VK_CLIENT_ID",
        json_schema_extra={"env": "VK_CLIENT_ID"},
    )
    vk_client_secret: str = Field(
        "<client_secret>",
        alias="VK_CLIENT_SECRET",
        json_schema_extra={"env": "VK_CLIENT_SECRET"},
    )
    vk_auth_base_url: str = Field(
        "https://oauth.yandex.ru/authorize",
        alias="VK_AUTH_BASE_URL",
        json_schema_extra={"env": "VK_AUTH_BASE_URL"},
    )
    vk_auth_token_url: str = Field(
        "https://oauth.yandex.ru/token",
        alias="VK_AUTH_TOKEN_URL",
        json_schema_extra={"env": "VK_AUTH_TOKEN_URL"},
    )
    vk_userinfo_url: str = Field(
        "https://login.yandex.ru/info",
        alias="VK_USERINFO_URL",
        json_schema_extra={"env": "VK_USERINFO_URL"},
    )
    
    enable_limiter: bool = Field(
        False,
        alias="ENABLE_LIMITER",
        json_schema_extra={"env": "ENABLE_LIMITER"},
    )
    
    
    super_admin_login: str = Field(
        "admin",
        alias="SUPER_USER_LOGIN",
        json_schema_extra={"env": "SUPER_USER_LOGIN"},
    )
    super_admin_password: str = Field(
        "password",
        alias="SUPER_USER_PASSWORD",
        json_schema_extra={"env": "SUPER_USER_PASSWORD"},
    )
    
    super_admin_email: EmailStr = Field(
        "2tK9H@example.com",
        alias="SUPER_USER_EMAIL",
        json_schema_extra={"env": "SUPER_USER_EMAIL"},
    )
    
    super_admin_tg_id: str = Field(
        "<tg_id>",
        alias="SUPER_USER_TG_ID",
        json_schema_extra={"env": "SUPER_USER_TG_ID"},
    )
    
    
    
settings = Settings()

@AuthJWT.load_config
def get_config():
    return settings