from functools import cache
from async_fastapi_jwt_auth import AuthJWT
from fastapi import Depends

from logic.services.user import BaseUserService
from infrastructure.storages.token import TokenStorage
from logic.services.auth import AuthService, BaseAuthService
from logic.dependencies.registrator import add_factory_to_mapper

@add_factory_to_mapper(BaseAuthService)
@cache
def create_auth_service(
    auth_jwt: AuthJWT = Depends(),
    token_storage: TokenStorage = Depends(),
    user_service: BaseUserService = Depends(),
) -> BaseAuthService:
    return AuthService(
        auth_jwt_service=auth_jwt,
        token_storage=token_storage,
        user_service=user_service,
    )