import pytest
from redis.asyncio import Redis

from schemas.user import UserCreateDTO
from logic.services.cache import RedisCacheService
from infrastructure.models.user import User


@pytest.mark.asyncio
async def test_cache_insert_get_delete(redis_client: Redis):
    async with redis_client as client:
        cache_service = RedisCacheService(_client=client, _model=User)
        
        user = UserCreateDTO(login="johndoe", password="password", email="john@example.com")
        await cache_service.set(key=user.login, value=user)
        u = await cache_service.get(key=user.login)
        assert u.login == user.login
        assert u.email == user.email
        assert u.tg_id is None
        await cache_service.delete(key=user.login)
        u = await cache_service.get(key=user.login)
        assert u is None