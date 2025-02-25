from abc import ABC, abstractmethod
from dataclasses import dataclass

from redis.asyncio import Redis
from redis.asyncio.client import Pipeline

from schemas.token import TokenJTI
from settings.config import settings


@dataclass
class TokenStorage(ABC):
    @abstractmethod
    async def store_token(self, *args, **kwargs):
        ...
        
    @abstractmethod
    async def get_token(self, *args, **kwargs):
        ...
        
    @abstractmethod
    async def check_expiration(self, *args, **kwargs):
        ...
        
        
        
@dataclass
class RedisTokenStorage(TokenStorage):
    _client: Redis
    
    async def store_token(self, *, token: TokenJTI) -> None:
        async def _store_token(pipeline: Pipeline):
            if token.access_token_jti:
                await pipeline.setex(
                    name=token.access_token_jti,
                    time=settings.access_expiratioin_seconds,
                    value=str(True)
                )
            if token.refresh_token_jti:
                await pipeline.setex(
                    name=token.refresh_token_jti,
                    time=settings.refresh_expiratioin_seconds,
                    value=str(True)
                )
        await self._client.transaction(_store_token)
        
    async def get_token(self, *, key: str) -> bool:
        return await self._client.get(key)
    
    async def check_expiration(self, *, jti: str) -> bool:
        return await self.get_token(key=jti) == True
    
    def __hash__(self):
        return hash(self._client)
    
    def __eq__(self, other):
        return hash(self) == hash(other)