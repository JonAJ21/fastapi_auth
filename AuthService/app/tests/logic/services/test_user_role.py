import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from schemas.role import RoleCreateDTO
from schemas.user import UserCreateDTO
from logic.services.role import RoleService
from logic.services.user import UserService
from infrastructure.repositories.role import PostgresRoleRepository
from infrastructure.repositories.user import PostgresUserRepository
from logic.unit_of_work.sqlalchemy import SqlAlchemyUnitOfWork
from logic.services.user_role import UserRoleService

@pytest.mark.asyncio
async def test_create_delete_update_get_role(db_session: AsyncSession):
    async with db_session as session:
        role_service = RoleService(
            _repository=PostgresRoleRepository(_session=session),
            _uow=SqlAlchemyUnitOfWork(_session=session),
        )
        user_service = UserService(
            _repository=PostgresUserRepository(_session=session),
            _uow=SqlAlchemyUnitOfWork(_session=session),
        )
        user_role_service = UserRoleService(
            _user_repository=PostgresUserRepository(_session=session),
            _role_repository=PostgresRoleRepository(_session=session),
            _uow=SqlAlchemyUnitOfWork(_session=session),
        )
        
        user = await user_service.create_user(
            UserCreateDTO(login="johndoe", password="password", email="john@example.com", tg_id="123")
        )
        role = await role_service.create_role(
            RoleCreateDTO(name="role", description="Role description"),
        )
        
        result = await user_role_service.assign_role_to_user(
            user_id=user.response.id, role_id=role.response.id
        )
        
        assert result.is_success == True
        
        fetched_user = await user_service.get_user(user_id=user.response.id)
        assert fetched_user is not None
        assert len(fetched_user.response.roles) == 1
        assert fetched_user.response.roles[0].name == "role"
        assert fetched_user.response.roles[0].description == "Role description"
        
        result = await user_role_service.remove_role_from_user(
            user_id=user.response.id, role_id=role.response.id
        )
        
        assert result.is_success == True
        
        fetched_user = await user_service.get_user(user_id=user.response.id)
        assert fetched_user is not None
        assert len(fetched_user.response.roles) == 0
        
        
        
        
        
        
        