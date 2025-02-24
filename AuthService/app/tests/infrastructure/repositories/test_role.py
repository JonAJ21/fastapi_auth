from uuid import uuid4
import pytest
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.models.role import Role
from logic.services.cache import RedisCacheService
from schemas.role import RoleCreateDTO
from infrastructure.repositories.role import PostgresCacheRoleRepository, PostgresRoleRepository


@pytest.mark.asyncio
async def test_get_user_with_roles(db_session: AsyncSession):
    async with db_session as session:
        repository = PostgresRoleRepository(_session=session)  
        role1 = await repository.insert(body=RoleCreateDTO(name="admin", description="Admin role"))
        role2 = await repository.insert(body=RoleCreateDTO(name="user", description="User role"))
        fetched_role_data = await repository.get_role_by_name(name="admin")
        assert fetched_role_data.description == role1.description
        fetched_role_data = await repository.get_role_by_name(name="user")
        assert fetched_role_data.description == role2.description
        fetched_role_data = await repository.get_role_by_name(name="super-user")
        assert fetched_role_data is None
        
@pytest.mark.asyncio
async def test_get_user_with_roles(db_session: AsyncSession, ):
    async with db_session as session:
        repository = PostgresRoleRepository(_session=session)  
        role1 = await repository.insert(body=RoleCreateDTO(name="admin", description="Admin role"))
        role2 = await repository.insert(body=RoleCreateDTO(name="user", description="User role"))
        fetched_role_data = await repository.get_role_by_name(name="admin")
        assert fetched_role_data.description == role1.description
        fetched_role_data = await repository.get_role_by_name(name="user")
        assert fetched_role_data.description == role2.description
        fetched_role_data = await repository.get_role_by_name(name="super-user")
        assert fetched_role_data is None
        
@pytest.mark.asyncio
async def test_get_user_with_roles(db_session: AsyncSession, redis_client: Redis):
    async with db_session as session:
        async with redis_client as client:
            repository = PostgresCacheRoleRepository(
                _session=session,
                _cache_service=RedisCacheService(
                    _client=client,
                    _model=Role
                )
            )
             
            role1 = await repository.insert(body=RoleCreateDTO(name="admin", description="Admin role"))
            role2 = await repository.insert(body=RoleCreateDTO(name="user", description="User role"))
            fetched_role_data = await repository.get_role_by_name(name="admin")
            assert fetched_role_data.description == role1.description
            fetched_role_data = await repository.get_role_by_name(name="user")
            assert fetched_role_data.description == role2.description
            fetched_role_data = await repository.get_role_by_name(name="super-user")
            assert fetched_role_data is None
        
@pytest.mark.asyncio
async def test_get_user_with_roles(db_session: AsyncSession, redis_client: Redis ):
    async with db_session as session:
        async with redis_client as client:
            repository = PostgresCacheRoleRepository(
                _session=session,
                _cache_service=RedisCacheService(
                    _client=client,
                    _model=Role
                )
            )
            role1 = await repository.insert(body=RoleCreateDTO(name="admin", description="Admin role"))
            role2 = await repository.insert(body=RoleCreateDTO(name="user", description="User role"))
            fetched_role_data = await repository.get_role_by_name(name="admin")
            assert fetched_role_data.description == role1.description
            fetched_role_data = await repository.get_role_by_name(name="user")
            assert fetched_role_data.description == role2.description
            fetched_role_data = await repository.get_role_by_name(name="super-user")
            assert fetched_role_data is None