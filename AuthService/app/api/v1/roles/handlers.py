from typing import Annotated, Any
from fastapi import APIRouter, Depends, HTTPException, Query, status

from infrastructure.models.role import Role
from schemas.result import GenericResult
from logic.services.auth import BaseAuthService, require_roles
from logic.services.role import BaseRoleService
from schemas.role import RoleBase, RoleCreateDTO, RoleDTO, RoleUpdateDTO, Roles


router = APIRouter(
    tags=['Roles'],    
)

@router.get(
    "/",
    response_model=list[RoleBase],
    description="Display existing system roles",
    response_description="Information about available system roles",
    summary="Display existing system roles",
)
@require_roles([Roles.ADMIN, Roles.SUPER_ADMIN])
async def get_roles(
    skip: Annotated[int, Query(description="Items to skip", ge=0)] = 0,
    limit: Annotated[int, Query(description="Pagination page size", ge=1)] = 10,
    role_service: BaseRoleService = Depends(),
    auth_service: BaseAuthService = Depends(),
) -> list[RoleBase]:
    return await role_service.get_roles(skip=skip, limit=limit)


@router.get(
    "/{role_id}",
    response_model=RoleDTO,
    description="Issuing role information",
    response_description="Information about the role in the system",
    summary="Issuing role information",
)
@require_roles([Roles.ADMIN, Roles.SUPER_ADMIN])
async def get_role(
    role_id: Any,
    role_service: BaseRoleService = Depends(),
    auth_service: BaseAuthService = Depends(),
) -> RoleDTO | None:
    role: GenericResult[Role] = await role_service.get_role(role_id=role_id)
    if not role.is_success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=role.error.reason)
    return role.response


@router.post(
    "/",
    response_model=RoleDTO,
    description="Creating a role in the system",
    response_description="New Role Details",
    summary="Creating a role in the system",
)
@require_roles([Roles.ADMIN, Roles.SUPER_ADMIN])
async def create_role(
    role_data: RoleCreateDTO,
    role_service: BaseRoleService = Depends(),
    auth_service: BaseAuthService = Depends(),
):
    result = await role_service.create_role(role=role_data)
    if not result.is_success:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=result.error.reason)
    return result.response


@router.put(
    "/{role_id}",
    response_model=RoleDTO,
    description="Editing a role in the system",
    response_description="Edited role",
    summary="Editing a role",
)
@require_roles([Roles.ADMIN, Roles.SUPER_ADMIN])
async def update_role(
    role_id: Any,
    role_data: RoleUpdateDTO,
    role_service: BaseRoleService = Depends(),
    auth_service: BaseAuthService = Depends(),
):
    result = await role_service.update_role(role_id=role_id, role_dto=role_data)
    if not result.is_success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=result.error.reason
        )
        

@router.delete(
    "/{role_id}",
    response_model=RoleDTO,
    description="Removing a role from the system",
    summary="Removing a role from the system",
)
@require_roles([Roles.ADMIN, Roles.SUPER_ADMIN])
async def delete_role(
    role_id: Any,
    role_service: BaseRoleService = Depends(),
    auth_service: BaseAuthService = Depends(),
):
    return await role_service.delete_role(role_id=role_id)