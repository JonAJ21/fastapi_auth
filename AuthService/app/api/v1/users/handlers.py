from typing import Annotated
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.responses import JSONResponse

from schemas.token import TokenValidation
from infrastructure.models.user import User
from logic.services.user_role import BaseUserRoleService
from schemas.result import GenericResult, Result
from logic.services.auth import BaseAuthService, require_roles
from logic.services.user import BaseUserService
from schemas.role import Roles
from schemas.user import UserBase, UserDTO, UserHistoryDTO, UserUpdateDTO


router = APIRouter(
    tags=['Users'],    
)

@router.get(
    "/",
    description="Retrieve information about all users in the system",
    response_model=list[UserBase],
    response_description="List of user accounts in the system",
    tags=["Users"],
)
@require_roles([Roles.ADMIN, Roles.SUPER_ADMIN])
async def get_users(
    skip: Annotated[int, Query(description="Items to skip", ge=0)] = 0,
    limit: Annotated[int, Query(description="Pagination page size", ge=1)] = 10,
    user_service: BaseUserService = Depends(),
    auth_service: BaseAuthService = Depends(),
):
    return await user_service.get_users(skip=skip, limit=limit)

@router.get(
    "/profile",
    description="Retrieve information about the user's account",
    response_model=UserDTO,
    response_description="Details of the authenticated user",
    tags=["Users"],
    summary="Details of the user's account",
)
async def get_user_profile(auth_service: BaseAuthService = Depends()) -> UserDTO:
    result = await auth_service.get_user()
    return result


@router.get(
    "/profile/history",
    description="Retrieve the user's login history",
    response_model=list[UserHistoryDTO],
    response_description="List of user logins",
    tags=["Users"],
    summary="Retrieve the user's login history",
)
async def get_user_profile_history(
    user_service: BaseUserService = Depends(),
    auth_service: BaseAuthService = Depends(),
    skip: Annotated[int, Query(description="Items to skip", ge=0)] = 0,
    limit: Annotated[int, Query(description="Pagination page size", ge=1)] = 10,
):
    user = await auth_service.get_user()
    result = await user_service.get_user_history(
        user_id=user.id, skip=skip, limit=limit
    )
    return result


@router.get(
    "/{user_id}/history",
    description="Retrieve the login history of a user",
    response_model=list[UserHistoryDTO],
    response_description="List of user logins",
    tags=["Administrator"],
    summary="Retrieve the login history of a user",
)
@require_roles([Roles.ADMIN, Roles.SUPER_ADMIN])
async def get_user_history(
    user_id: UUID,
    skip: Annotated[int, Query(description="Items to skip", ge=0)] = 0,
    limit: Annotated[int, Query(description="Pagination page size", ge=1)] = 10,
    user_service: BaseUserService = Depends(),
    auth_service: BaseAuthService = Depends(),
):
    result = await user_service.get_user_history(
        user_id=user_id, skip=skip, limit=limit
    )
    return result

@router.get(
    "/{user_id}",
    description="Retrieve information about a user. Requires administrative privileges",
    response_model=UserDTO,
    tags=["Administrator"],
    response_description="Details of the registered user",
    summary="Details of the user's account. Administrative functionality",
)
@require_roles([Roles.ADMIN, Roles.SUPER_ADMIN])
async def get_user(
    user_id: UUID,
    user_service: BaseUserService = Depends(),
    auth_service: BaseAuthService = Depends(),
) -> User:
    user: GenericResult[User] = await user_service.get_user(user_id=user_id)
    if not user.is_success:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=user.error.reason)
    return user.response


@router.put(
    "/profile",
    response_model=UserDTO,
    description="Update user information",
    tags=["Users"],
    response_description="Updated user account details",
    summary="Update user account details",
)
async def update_user_profile(
    user_info: UserUpdateDTO,
    user_service: BaseUserService = Depends(),
    auth_service: BaseAuthService = Depends(),
) -> UserDTO:
    user = await auth_service.get_user()
    user_result: GenericResult[User] = await user_service.update_user(
        user_id=user.id, user_dto=user_info
    )
    if not user_result.is_success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=user.error.reason
        )
    return user_result.response


@router.put(
    "/{user_id}/role/{role_id}",
    description="Assign a role to a user",
    tags=["Administrator"],
    summary="Assign an additional role to a user",
)
@require_roles([Roles.ADMIN, Roles.SUPER_ADMIN])
async def assign_role_to_user(
    user_id: UUID,
    role_id: UUID,
    user_role_service: BaseUserRoleService = Depends(),
    auth_service: BaseAuthService = Depends(),
):
    result: Result = await user_role_service.assign_role_to_user(
        user_id=user_id, role_id=role_id
    )
    if not result.is_success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=result.error.reason
        )
    return JSONResponse(status_code=status.HTTP_200_OK, content={})


@router.delete(
    "/{user_id}/role/{role_id}",
    description="Revoke a role from a user",
    tags=["Administrator"],
    summary="Revoke a role from a user",
)
@require_roles([Roles.ADMIN, Roles.SUPER_ADMIN])
async def remove_role_from_user(
    user_id: UUID,
    role_id: UUID,
    user_role_service: BaseUserRoleService = Depends(),
    auth_service: BaseAuthService = Depends(),
):
    result: Result = await user_role_service.remove_role_from_user(
        user_id=user_id, role_id=role_id
    )
    if not result.is_success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=result.error.reason
        )
    return JSONResponse(status_code=status.HTTP_200_OK, content={})

@router.post(
    "/info",
    description="Retrieve information about a registered user based on the provided JWT token",
    summary="Retrieve user data",
    tags=["Users"],
)
async def get_user_data(
    token_data: TokenValidation, auth_service: BaseAuthService = Depends()
) -> UserDTO:
    try:
        user = await auth_service.get_auth_user(token_data.access_token)
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        return user
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.message)

@router.delete(
    "/profile",
    description="Delete the user's account",
    summary="Delete the user's account",
    tags=["Users"],
)
async def delete_user_profile(
    user_service: BaseUserService = Depends(), auth_service: BaseAuthService = Depends()
):
    user = await auth_service.get_user()
    await user_service.delete_user(user_id=user.id)
    await auth_service.logout()
    return JSONResponse(status_code=status.HTTP_200_OK, content={})


@router.delete(
    "/{user_id}",
    description="Delete a user's account. Requires administrative privileges.",
    summary="Delete a user's account",
    tags=["Administrator"],
)
@require_roles([Roles.ADMIN, Roles.SUPER_ADMIN])
async def delete_user(
    user_id: UUID,
    user_service: BaseUserService = Depends(),
    auth_service: BaseAuthService = Depends(),
):
    await user_service.delete_user(user_id=user_id)
    return JSONResponse(status_code=status.HTTP_200_OK, content={})