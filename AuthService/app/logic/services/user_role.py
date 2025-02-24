from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any

from infrastructure.repositories.role import BaseRoleRepository
from logic.unit_of_work.base import BaseUnitOfWork
from infrastructure.repositories.user import BaseUserRepository
from schemas.result import Error, Result


@dataclass
class BaseUserRoleService(ABC):
    
    @abstractmethod
    async def assign_role_to_user(self, user_id: Any, role_id: Any) -> Result:
        ...
        
    @abstractmethod
    async def remove_role_from_user(self, user_id: Any, role_id: Any) -> Result:
        ...
        
@dataclass
class UserRoleService(BaseUserRoleService):
    _user_repository: BaseUserRepository
    _role_repository: BaseRoleRepository
    _uow: BaseUnitOfWork
    
    async def assign_role_to_user(self, user_id: Any, role_id: Any) -> Result:
        user = await self._user_repository.get(id=user_id)
        role = await self._role_repository.get(id=role_id)
        if not user:
            return Result.failure(
                Error(error_code="USER_NOT_FOUND", reason="User not found")
            )
        if not role:
            return Result.failure(
                Error(error_code="ROLE_NOT_FOUND", reason="Role not found")
            )
        user.assign_role(role)
        await self._uow.commit()
        return Result.success()
        
    async def remove_role_from_user(self, user_id: Any, role_id: Any) -> Result:
        user = await self._user_repository.get(id=user_id)
        role = await self._role_repository.get(id=role_id)
        if not user:
            return Result.failure(
                Error(error_code="USER_NOT_FOUND", reason="User not found")
            )
        if not role:
            return Result.failure(
                Error(error_code="ROLE_NOT_FOUND", reason="Role not found")
            )
        user.remove_role(role)
        await self._uow.commit()
        return Result.success()