from functools import cache

from fastapi import Depends
from redis.asyncio import Redis


from infrastructure.database.redis import get_redis
from infrastructure.storages.token import RedisTokenStorage, TokenStorage
from logic.dependencies.registrator import add_factory_to_mapper


@add_factory_to_mapper(TokenStorage)
@cache
def create_token_storage(redis_client: Redis = Depends(get_redis)) -> TokenStorage:
    return RedisTokenStorage(_client=redis_client)