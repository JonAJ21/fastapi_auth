from abc import ABC, abstractmethod
from dataclasses import dataclass
import json
from typing import Generic, Type

from redis.asyncio import Redis

from infrastructure.repositories.base import CreateSchemaType
from schemas.result import ModelType


@dataclass
class BaseCacheService(ABC):
    @abstractmethod
    async def get(self, *args, **kwargs):
        ...

    @abstractmethod
    async def set(self, *args, **kwargs):
        ...
        
    @abstractmethod
    async def delete(self, *args, **kwargs):
        ...
        
@dataclass
class RedisCacheService(BaseCacheService, Generic[ModelType, CreateSchemaType]):
    _client: Redis
    _model: Type[ModelType]
    
    async def get(self, *, key: str) -> ModelType | None:
        document = await self._client.get(key)
        if not document:
            return None
        return self._model(**json.loads(document))
    
    async def set(self, *, key: str, value: CreateSchemaType) -> None:
        await self._client.set(key, json.dumps(value.model_dump()))
        
    async def delete(self, *, key: str) -> None:
        if await self._client.exists(key):
            await self._client.delete(key)
