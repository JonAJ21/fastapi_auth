from functools import cache

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from redis.asyncio import Redis

from infrastructure.database.postgres import get_session
from infrastructure.database.redis import get_redis
from infrastructure.models.user import User
from infrastructure.repositories.user import PostgresCacheUserRepository, PostgresUserRepository
from logic.dependencies.registrator import add_factory_to_mapper
from logic.services.cache import RedisCacheService
from logic.services.user import BaseUserService, UserService
from logic.unit_of_work.sqlalchemy import SqlAlchemyUnitOfWork


@add_factory_to_mapper(BaseUserService)
@cache
def create_user_service(
    session: AsyncSession = Depends(get_session), redis: Redis = Depends(get_redis)
) -> BaseUserService:
    cache_service = RedisCacheService(_client=redis, _model=User)
    unit_of_work = SqlAlchemyUnitOfWork(session=session)
    cached_repository = PostgresCacheUserRepository(
        _session=session,
        _model=User,
        _cache_service=cache_service,    
    )
    return UserService(_repository=cached_repository, _uow=unit_of_work)