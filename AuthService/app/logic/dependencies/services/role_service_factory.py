from functools import cache

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from redis.asyncio import Redis

from infrastructure.database.postgres import get_session
from infrastructure.database.redis import get_redis
from infrastructure.models.role import Role
from infrastructure.repositories.role import PostgresCacheRoleRepository, PostgresRoleRepository
from logic.dependencies.registrator import add_factory_to_mapper
from logic.services.cache import RedisCacheService
from logic.services.role import BaseRoleService, RoleService
from logic.unit_of_work.sqlalchemy import SqlAlchemyUnitOfWork


@add_factory_to_mapper(BaseRoleService)
@cache
def create_role_service(
    session: AsyncSession = Depends(get_session), redis: Redis = Depends(get_redis)
) -> BaseRoleService:
    cache_service = RedisCacheService(client=redis, model=Role)
    cached_repository = PostgresCacheRoleRepository(
        _session=session,
        _model=Role,
        _cache_service=cache_service
    )
    unit_of_work = SqlAlchemyUnitOfWork(session=session)
    return RoleService(repository=cached_repository, uow=unit_of_work)