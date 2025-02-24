import pytest
from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession

from schemas.user import UserCreateDTO
from infrastructure.models.user import User
from infrastructure.repositories.postgre import PostgresRepository

@pytest.mark.asyncio
async def test_user_insert_get(db_session: AsyncSession):
    async with db_session as session:
        repository = PostgresRepository(_session=session, _model=User)
        user = await repository.insert(body=UserCreateDTO(login="johndoe", password="password", email="john@example.com"))     
        assert user is not None
        assert user.password != "password"
        assert user.email == "john@example.com"
        u = await repository.get(id=user.id)
        assert u is not None
        assert u.id == user.id
        
@pytest.mark.asyncio
async def test_user_insert_delete_get(db_session: AsyncSession):
    async with db_session as session:
        repository = PostgresRepository(_session=session, _model=User)
        user = await repository.insert(body=UserCreateDTO(login="johndoe", password="password", email="john@example.com"))     
        assert user is not None
        assert user.password != "password"
        assert user.email == "john@example.com"
        u = await repository.get(id=user.id)
        assert u is not None
        assert u.id == user.id
        
        await repository.delete(id=user.id)
        u = await repository.get(id=user.id)
        assert u is None
       
@pytest.mark.asyncio
async def test_user_insert_gets(db_session: AsyncSession):
    async with db_session as session:
        repository = PostgresRepository(_session=session, _model=User)
        user1 = await repository.insert(body=UserCreateDTO(login="1", password="password", email="1@example.com"))
        user2 = await repository.insert(body=UserCreateDTO(login="2", password="password", email="2@example.com")) 
        user3 = await repository.insert(body=UserCreateDTO(login="3", password="password", email="3@example.com"))  
        
        u = await repository.gets(skip = 1, limit = 2)
        assert len(u) == 2   
        
        u = await repository.gets(skip = 0)
        assert len(u) == 3
        
        assert u[2].id == user3.id
