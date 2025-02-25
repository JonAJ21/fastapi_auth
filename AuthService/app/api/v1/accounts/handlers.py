from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Header, status
from fastapi.responses import JSONResponse

from logic.services.auth import BaseAuthService
from schemas.auth import RefreshRequestDTO, UserLoginDTO
from infrastructure.models.user import User
from logic.dependencies.main import build_dependencies
from logic.services.user import BaseUserService
from schemas.result import GenericResult
from schemas.user import UserBase, UserCreateDTO
from schemas.token import Token
from logic.dependencies.registrator import dependencies_container

router = APIRouter(
    tags=['Accounts'],    
)

@router.post(
    "/register",
    response_model=UserBase,
    description="Register new user",
    summary="Creating account for new user",
    dependencies=build_dependencies(),
)
async def register(
    user: UserCreateDTO, user_service: BaseUserService = Depends()
) -> User:
    response: GenericResult[User] = await user_service.create_user(user_dto=user)
    if response.is_success:
        return response.response
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST, detail=response.error.reason
    )

@router.post(
    "/login",
    response_model=Token,
    description="User auth",
    summary="User JWT auth",
    response_description="Access and refresh tokens",
    dependencies=build_dependencies(),
)
async def login(
    user_login: UserLoginDTO,
    user_agent: Annotated[str | None, Header()] = None,
    auth: BaseAuthService = Depends(),
):
    token: GenericResult[Token] = await auth.login(
        login=user_login.login,
        password=user_login.password,
        user_agent=user_agent,
    )
    if not token.is_success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="login or/and password incorrect"
        )

    return token.response

@router.post(
    "/refresh",
    response_model=Token,
    description="Issuing new tokens if the access token is expired",
    response_description="Access and refresh tokens",
    dependencies=build_dependencies(),
)
async def refresh(
    token: RefreshRequestDTO,
    auth_service: BaseAuthService = Depends(),
):
    return await auth_service.refresh(token.jti)

@router.post(
    "/logout",
    description="User logout",
)
async def logout(auth_service: BaseAuthService = Depends()):
    await auth_service.logout()
    return JSONResponse(status_code=status.HTTP_200_OK, content={})