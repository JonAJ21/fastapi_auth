from functools import cache

from fastapi import Depends
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.database.redis import get_redis
from infrastructure.models.role import Role
from infrastructure.database.postgres import get_session
from infrastructure.models.user import User
from infrastructure.repositories.role import PostgresCacheRoleRepository, PostgresRoleRepository
from infrastructure.repositories.user import PostgresCacheUserRepository, PostgresUserRepository
from logic.dependencies.registrator import add_factory_to_mapper
from logic.services.cache import RedisCacheService
from logic.services.user_role import BaseUserRoleService, UserRoleService
from logic.unit_of_work.sqlalchemy import SqlAlchemyUnitOfWork


@add_factory_to_mapper(BaseUserRoleService)
@cache
def create_user_role_service(
    session: AsyncSession = Depends(get_session), redis: Redis = Depends(get_redis)
) -> BaseUserRoleService:
    user_cache_service = RedisCacheService(_client=redis, _model=User)
    cached_user_repository = PostgresCacheUserRepository(
        _session=session,
        _model=User,
        _cache_service=user_cache_service
    )
    role_cache_service = RedisCacheService(_client=redis, _model=Role)
    cached_role_repository = PostgresCacheRoleRepository(
        _session=session,
        _model=Role,
        _cache_service=role_cache_service
    )
    unit_of_work = SqlAlchemyUnitOfWork(_session=session)
    return UserRoleService(
        _user_repository=cached_user_repository,
        _role_repository=cached_role_repository,
        _uow=unit_of_work,
    )