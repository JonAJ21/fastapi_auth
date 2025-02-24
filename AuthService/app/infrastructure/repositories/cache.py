from dataclasses import dataclass
from typing import Any, Generic, List, Type

from logic.services.cache import BaseCacheService
from infrastructure.repositories.postgre import PostgresRepository
from infrastructure.repositories.base import CreateSchemaType, ModelType


@dataclass 
class PostgresCacheRepository(
    PostgresRepository[ModelType, CreateSchemaType],
    Generic[ModelType, CreateSchemaType],
):
    
    _cache_service: BaseCacheService
    
    async def gets(self, *, skip: int = 0, limit: int = 100) -> List[ModelType]:
        return await super().gets(skip=skip, limit=limit)
    
    async def get(self, *, id: Any) -> ModelType | None:
        key = f"{self._model.__name__}_{id}"
        entity = await self._cache_service.get(key=key)
        if not entity:
            entity = await super().get(id=id)
        return entity
    
    async def insert(self, *, body: CreateSchemaType) -> ModelType:
        return await super().insert(body=body)
    
    async def delete(self, *, id: Any) -> None:
        await super().delete(id=id)