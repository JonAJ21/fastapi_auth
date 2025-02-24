import pytest
import pytest_asyncio
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from redis.asyncio import Redis
from infrastructure.database.postgres import Base

from tests.config import settings

# Создаем движок базы данных для тестов
TEST_DATABASE_URL = str(settings.postgres_connection)
ALEMBIC_INI_PATH = "/app/alembic.ini"



@pytest.fixture(scope="module", autouse=True)
def prepare_database():
    sync_engine = create_engine(TEST_DATABASE_URL.replace("+asyncpg", ""), echo=True)
    Base.metadata.create_all(bind=sync_engine)
    yield
    Base.metadata.drop_all(bind=sync_engine)
    

@pytest_asyncio.fixture
async def db_session(scope="module"):
    async_engine = create_async_engine(TEST_DATABASE_URL, echo=True)
    async_session= sessionmaker(
        bind=async_engine, class_=AsyncSession, expire_on_commit=False
    )
    
    """Фикстура для создания сессии с БД."""
    async with async_session() as session:
        yield session
        await session.rollback()

@pytest_asyncio.fixture(scope="module")
async def redis_client():
    client = Redis(
        host=settings.redis_host,
        port=6379,
        password=settings.redis_password,
        db=0
    )
    async with client:
        yield client
        await client.flushdb()
        await client.aclose()