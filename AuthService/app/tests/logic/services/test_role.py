import pytest

from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.repositories.role import PostgresRoleRepository
from schemas.role import RoleCreateDTO, RoleUpdateDTO
from logic.services.role import RoleService

from logic.unit_of_work.sqlalchemy import SqlAlchemyUnitOfWork

@pytest.mark.asyncio
async def test_create_delete_update_get_role(db_session: AsyncSession):
    async with db_session as session:
        role_service = RoleService(
            _repository=PostgresRoleRepository(_session=session),
            _uow=SqlAlchemyUnitOfWork(_session=session),
        )
        
        result = await role_service.get_roles(skip=0, limit=10)
        assert result is not None
        assert len(result) == 0
        
        result = await role_service.create_role(
            RoleCreateDTO(name="user", description="User role")
        )
        
        result = await role_service.get_role(result.response.id)
        assert result is not None
        assert result.response.name == "user"
        assert result.response.description == "User role"
        
        result = await role_service.update_role(
            role_id=result.response.id,
            role_dto=RoleUpdateDTO(name="admin", description="Admin role")
        )
        
        assert result.is_success == True
        
        result = await role_service.get_role(result.response.id)
        assert result is not None
        print("\n\n\n\n\n", result.response.name, "\n\n\n\n\n")
        assert result.response.name == "admin"
        assert result.response.description == "Admin role"
        
        await role_service.delete_role(role_id=result.response.id)
        
        
        result = await role_service.get_role(result.response.id)
        assert result.is_success == False
        