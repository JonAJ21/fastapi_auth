from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any

from infrastructure.repositories.role import BaseRoleRepository
from logic.unit_of_work.base import BaseUnitOfWork
from schemas.result import Error, GenericResult
from schemas.role import RoleCreateDTO
from infrastructure.models.role import Role


@dataclass
class BaseRoleService(ABC):
    
    @abstractmethod
    async def get_roles(self, *, skip: int, limit: int) -> list[Role]:
        ...
        
    @abstractmethod
    async def create_role(self, role: RoleCreateDTO) -> GenericResult[Role]:
        ...
        
    @abstractmethod
    async def get_role(self, role_id: Any) -> GenericResult[Role]:
        ...
        
    @abstractmethod
    async def update_role(
        self, role_id: Any, role: RoleCreateDTO
    ) -> GenericResult[Role]:
        ...
        
    @abstractmethod
    async def delete_role(self, role_id: Any) -> None:
        ...
        
@dataclass
class RoleService(BaseRoleService):
    _repository: BaseRoleRepository
    _uow: BaseUnitOfWork
    
    async def get_roles(self, *, skip: int, limit: int) -> list[Role]:
        return await self._repository.gets(skip=skip, limit=limit)
    
    async def create_role(self, role: RoleCreateDTO) -> GenericResult[Role]:
        role_db = await self._repository.get_role_by_name(name=role.name)
        response = GenericResult.failure(
            Error(error_code="ROLE_ALREADY_EXISTS", reason="Role already exists")
        )
        if not role_db:
            role_db = await self._repository.insert(body=role)
            await self._uow.commit()
            response = GenericResult.success(role_db)
        return response
    
    async def get_role(self, role_id: Any) -> GenericResult[Role]:
        role = await self._repository.get(id=role_id)
        if not role:
            return GenericResult.failure(
                Error(error_code="ROLE_NOT_FOUND", reason="Role not found")
            )
        return GenericResult.success(role)
    
    async def update_role(self, role_id, role):
        return await super().update_role(role_id, role)
    
    async def update_role(
        self, role_id: Any, role: RoleCreateDTO
    )-> GenericResult[Role]:
        role = await self._repository.get(id=role_id)
        response = GenericResult.failure(
            Error(error_code="ROLE_NOT_FOUND", reason="Role not found")
        )
        if role:
            role.update(**role.model_dump())
            await self._uow.commit()
            response = GenericResult.success(role)
        return response
    
    async def delete_role(self, role_id: Any) -> None:
        await self._repository.delete(id=role_id)
        return await self._uow.commit()