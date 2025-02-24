from uuid import uuid4
import pytest

from sqlalchemy.ext.asyncio import AsyncSession

from schemas.social import SocialNetworks, SocialUser
from schemas.user import UserCreateDTO, UserHistoryCreateDTO, UserUpdateDTO, UserUpdatePasswordDTO
from logic.unit_of_work.sqlalchemy import SqlAlchemyUnitOfWork
from infrastructure.repositories.user import PostgresUserRepository
from logic.services.user import UserService


@pytest.mark.asyncio
async def test_create_delete_user(db_session: AsyncSession):
    async with db_session as session:
        user_service = UserService(
            _repository=PostgresUserRepository(_session=session),
            _uow=SqlAlchemyUnitOfWork(_session=session),
        )
        positive_result = await user_service.create_user(
            UserCreateDTO(login="johndoe", password="password", email="john@example.com", tg_id="123")
        )
        assert positive_result is not None
        assert positive_result.is_success is True
        assert positive_result.error_code is None
        assert positive_result.response is not None
        assert positive_result.response.tg_id == "123"
        failure_result = await user_service.create_user(
            UserCreateDTO(login="johndoe", password="password", email="john@example.com", tg_id="123")
        )
        assert failure_result.is_success is False
        assert failure_result.error_code is not None
            
        await user_service.delete_user(user_id=positive_result.response.id)
            
            
@pytest.mark.asyncio
async def test_get_user(db_session: AsyncSession):
    async with db_session as session:
        user_service = UserService(
            _repository=PostgresUserRepository(_session=session),
            _uow=SqlAlchemyUnitOfWork(_session=session),
        )

        result = await user_service.get_user(user_id=uuid4())
        assert result is not None
        assert result.is_success is False
        assert result.error_code is not None
        assert result.response is None
        result = await user_service.create_user(
            UserCreateDTO(login="johndoe", password="password", email="john@example.com", tg_id="123")
        )
            
        user_id = result.response.id
            
        result = await user_service.get_user(user_id=user_id)
        assert result is not None
        assert result.is_success is True
        assert result.error_code is None
        assert result.response.login == "johndoe"
        
        result = await user_service.get_user_by_login(login="johndoe")
        assert result is not None
        assert result.id == user_id
        
        result = await user_service.get_users()
        assert len(result) == 1
        assert result[0].id == user_id
        
        await user_service.delete_user(user_id=result[0].id)
            
@pytest.mark.asyncio
async def test_login_history(db_session: AsyncSession):
    async with db_session as session:
        user_service = UserService(
            _repository=PostgresUserRepository(_session=session),
            _uow=SqlAlchemyUnitOfWork(_session=session),
        )
        id = uuid4()
        result = await user_service.insert_user_login(
            user_id=id,
            history_row=UserHistoryCreateDTO(
                user_id=id,
                user_agent="Mozila",
                user_device_type="web",
                success=True
            )
        )
        assert result.is_success is False
        
        result = await user_service.create_user(
            UserCreateDTO(login="johndoe", password="password", email="john@example.com", tg_id="123")
        )
        result = await user_service.insert_user_login(
            user_id=result.response.id,
            history_row=UserHistoryCreateDTO(
                user_id=result.response.id,
                user_agent="Mozila",
                user_device_type="web",
                success=True
            )
        )
        assert result.is_success == True
        assert result.response.user_device_type == "web"
        
        result = await user_service.get_user_history(user_id=result.response.user_id)
        assert len(result) == 1
        assert result[0].user_agent == "Mozila"

@pytest.mark.asyncio
async def test_password(db_session: AsyncSession):
    async with db_session as session:
        user_service = UserService(
            _repository=PostgresUserRepository(_session=session),
            _uow=SqlAlchemyUnitOfWork(_session=session),
        )
        
        result = await user_service.create_user(
            UserCreateDTO(login="dory", password="password", email="dory@example.com", tg_id="123")
        )
        assert result.is_success == True
        old_password_hash = result.response.password
        
        result = await user_service.update_password(
            user_id = result.response.id,
            password_user=UserUpdatePasswordDTO(
                old_password="password",
                new_password="new_password"
            )
        )
        assert result.is_success == True
        
        result = await user_service.get_user(user_id=result.response.id)
        assert result.response.password != old_password_hash
        
        
          
        
@pytest.mark.asyncio
async def test_login_history(db_session: AsyncSession):
    async with db_session as session:
        user_service = UserService(
            _repository=PostgresUserRepository(_session=session),
            _uow=SqlAlchemyUnitOfWork(_session=session),
        )
        
        result = await user_service.get_or_create_user(
            social=SocialUser(
                id=str(uuid4()),
                login="johndoe",
                email="john@example.com",
                social_name=SocialNetworks.VK
            )
        )
        
        assert result.is_success == True
        assert result.response.email == "john@example.com"
        
        result = await user_service.update_user(
            user_id=result.response.id,
            user_dto=UserUpdateDTO(
                email="dory@example.com",
            )
        )
           
        assert result.is_success == True    
        assert result.response.email == "dory@example.com"
        
        result = await user_service.get_user_by_login(login="johndoe")
        assert result.email == "dory@example.com"
        

            
            
        