from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Type

from sqlalchemy import select

from logic.services.cache import BaseCacheService
from infrastructure.repositories.cache import PostgresCacheRepository
from infrastructure.repositories.postgre import PostgresRepository
from schemas.role import RoleCreateDTO
from infrastructure.models.role import Role
from infrastructure.repositories.base import BaseRepository, ModelType


@dataclass
class BaseRoleRepository(BaseRepository, ABC):
    @abstractmethod
    async def get_role_by_name(self, *, name: str) -> Role | None:
        ...
        
        
@dataclass
class PostgresRoleRepository(PostgresRepository[Role, RoleCreateDTO], BaseRoleRepository):
    _model: Type[ModelType] = Role
    
    async def get_role_by_name(self, *, name: str) -> Role | None:
        statement = select(self._model).where(self._model.name == name)
        return (await self._session.execute(statement)).scalar_one_or_none()
    
    def __hash__(self):
        return hash((self._model))
        
    def __eq__(self, other):
        return hash(self) == hash(other)

@dataclass
class PostgresCacheRoleRepository(
    PostgresCacheRepository[Role, RoleCreateDTO], PostgresRoleRepository
):  
    _cache_service: BaseCacheService | None = None
    _model: Type[ModelType] = Role
    
    async def get_role_by_name(self, *, name: str) -> Role | None:
        key = f"{self._model.__name__}_{name}"
        if self._cache_service is not None:
            entity = await self._cache_service.get(key=key)
        if not entity:
            entity = await super().get_role_by_name(name=name)
        return entity
    
    def __hash__(self):
        return hash((self._model, self._cache_service))
        
    def __eq__(self, other):
        return hash(self) == hash(other)