import pytest
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.models.user import User
from logic.services.cache import RedisCacheService
from schemas.social import SocialCreateDTO, SocialNetworks
from schemas.user import UserCreateDTO, UserHistoryCreateDTO
from infrastructure.repositories.user import PostgresCacheUserRepository, PostgresUserRepository

@pytest.mark.asyncio
async def test_get_by_login(db_session: AsyncSession):
    async with db_session as session:
        repository = PostgresUserRepository(_session=session)
        
        user = await repository.insert(body=UserCreateDTO(login="johndoe", password="password", email="john@example.com"))
        assert user is not None
        
        fetched_user = await repository.get_by_login(login="johndoe")
        assert fetched_user is not None
        assert fetched_user.login == "johndoe"
        assert fetched_user.email == "john@example.com"
    
@pytest.mark.asyncio
async def test_get_user_with_roles(db_session: AsyncSession):
    async with db_session as session:
        repository = PostgresUserRepository(_session=session)
        
        user = await repository.insert(body=UserCreateDTO(login="johndoe", password="password", email="john@example.com"))
        login_result = await repository.insert_user_login(
            user_id=user.id, 
            data=UserHistoryCreateDTO(
                user_id=user.id,
                user_agent="Chrome",
                user_device_type="web",
                success=True
            )
        )
        social_result = await repository.insert_user_social(
            user_id=user.id, 
            data=SocialCreateDTO(
                user_id=user.id,
                social_id="3819",
                social_name=SocialNetworks.YANDEX,
            )
        )
        fetched_user_data = await repository.get(id=user.id)
        assert fetched_user_data.social_accounts[0].social_name == SocialNetworks.YANDEX
        assert fetched_user_data.social_accounts[0].social_id == "3819"
        assert fetched_user_data.history[0].user_agent == "Chrome"
        assert fetched_user_data.history[0].user_device_type == "web"
        assert fetched_user_data.history[0].success
        
        history = await repository.get_user_history(user_id=user.id)
        assert history[0].user_agent == "Chrome"
        assert history[0].user_device_type == "web"
        assert history[0].success
        
        social = await repository.get_user_social(social_id="3819", social_name=SocialNetworks.YANDEX)
        assert social.user_id == user.id
        
@pytest.mark.asyncio
async def test_get_by_login(db_session: AsyncSession, redis_client: Redis):
    async with db_session as session:
        async with redis_client as client:
            repository = PostgresCacheUserRepository(
                _session=session,
                _cache_service=RedisCacheService(
                    _client=client,
                    _model=User
                )
            )
            user = await repository.insert(body=UserCreateDTO(login="johndoe", password="password", email="john@example.com"))
            assert user is not None
            fetched_user = await repository.get_by_login(login="johndoe")
            assert fetched_user is not None
            assert fetched_user.login == "johndoe"
            assert fetched_user.email == "john@example.com"
            
@pytest.mark.asyncio
async def test_get_user_with_roles(db_session: AsyncSession, redis_client: Redis):
    async with db_session as session:
        async with redis_client as client:
            repository = PostgresCacheUserRepository(
                _session=session,
                _cache_service=RedisCacheService(
                    _client=client,
                    _model=User
                )
            )
            user = await repository.insert(body=UserCreateDTO(login="johndoe", password="password", email="john@example.com"))
            login_result = await repository.insert_user_login(
                user_id=user.id, 
                data=UserHistoryCreateDTO(
                    user_id=user.id,
                    user_agent="Chrome",
                    user_device_type="web",
                    success=True
                )
            )
            social_result = await repository.insert_user_social(
                user_id=user.id, 
                data=SocialCreateDTO(
                    user_id=user.id,
                    social_id="3819",
                    social_name=SocialNetworks.YANDEX,
                )
            )
            fetched_user_data = await repository.get(id=user.id)
            assert fetched_user_data.social_accounts[0].social_name == SocialNetworks.YANDEX
            assert fetched_user_data.social_accounts[0].social_id == "3819"
            assert fetched_user_data.history[0].user_agent == "Chrome"
            assert fetched_user_data.history[0].user_device_type == "web"
            assert fetched_user_data.history[0].success
            
            history = await repository.get_user_history(user_id=user.id)
            assert history[0].user_agent == "Chrome"
            assert history[0].user_device_type == "web"
            assert history[0].success
            
            social = await repository.get_user_social(social_id="3819", social_name=SocialNetworks.YANDEX)
            assert social.user_id == user.id