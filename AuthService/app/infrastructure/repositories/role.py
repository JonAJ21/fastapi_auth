from abc import ABC, abstractmethod
from dataclasses import dataclass

from sqlalchemy import select

from infrastructure.repositories.cache import CacheRepository
from infrastructure.repositories.postgre import PostgresRepository
from schemas.role import RoleCreateDTO
from infrastructure.models.role import Role
from infrastructure.repositories.base import BaseRepository


@dataclass
class BaseRoleRepository(BaseRepository, ABC):
    @abstractmethod
    async def get_role_by_name(self, *, name: str) -> Role | None:
        ...
        
        
@dataclass
class RoleRepository(PostgresRepository[Role, RoleCreateDTO], BaseRoleRepository):
    _model = Role
    
    async def get_role_by_name(self, *, name: str) -> Role | None:
        statement = select(self._model).where(self._model.name == name)
        return await self._session.execute(statement).scalar_one_or_none()
    

@dataclass
class CacheRoleRepository(
    CacheRepository[Role, RoleCreateDTO], BaseRoleRepository
):
    _model = Role
    
    async def get_role_by_name(self, *, name: str) -> Role | None:
        key = f"{self._model.__name__}_{name}"
        entity = await self._cache_service.get(key=key)
        if not entity:
            entity = await self._repository.get_role_by_name(name=name)
        return entity
    