from dataclasses import dataclass
from typing import Any, Generic, List, Type

from logic.services.cache import BaseCacheService
from infrastructure.repositories.postgre import PostgresRepository
from infrastructure.repositories.base import CreateSchemaType, ModelType


@dataclass 
class CacheRepository(
    PostgresRepository[ModelType, CreateSchemaType],
    Generic[ModelType, CreateSchemaType],
):
    _repository: PostgresRepository[ModelType, CreateSchemaType]
    _model: Type[ModelType]
    _cache_service: BaseCacheService
    
    async def gets(self, *, skip: int = 0, limit: int = 100) -> List[ModelType]:
        return await self._repository.get(skip=skip, limit=limit)
    
    async def get(self, *, id: Any) -> ModelType | None:
        key = f"{self._model.__name__}_{id}"
        entity = await self._cache_service.get(key=key)
        if not entity:
            entity = await self._repository.get(id=id)
        return entity
    
    async def insert(self, *, body: CreateSchemaType) -> ModelType:
        return await self._repository.insert(body=body)
    
    async def delete(self, *, id: Any) -> None:
        await self._repository.delete(id=id)