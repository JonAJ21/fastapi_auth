from typing import Any, Callable

from fastapi import Depends, FastAPI
from fastapi_limiter.depends import RateLimiter

from async_fastapi_jwt_auth import AuthJWT
from infrastructure.storages.token import TokenStorage
from logic.dependencies.services.auth_service_factory import create_auth_service
from logic.dependencies.services.role_service_factory import create_role_service
from logic.dependencies.services.token_storage_factory import create_token_storage
from logic.dependencies.services.user_role_service_factory import create_user_role_service
from logic.services.auth import BaseAuthService
from logic.services.role import RoleService
from logic.services.user_role import BaseUserRoleService
from logic.dependencies.services.user_service_factory import create_user_service
from logic.services.user import BaseUserService
from logic.dependencies.registrator import dependencies_container
from settings.config import settings



def setup_dependencies(app: FastAPI, mapper: dict[Any, Callable] | None = None) -> None:
    if mapper is None:
        dependencies_container[BaseUserService] = create_user_service
        dependencies_container[BaseUserRoleService] = create_user_role_service
        dependencies_container[TokenStorage] = create_token_storage
        dependencies_container[RoleService] = create_role_service
        dependencies_container[BaseAuthService] = create_auth_service
        
        mapper = dependencies_container
    for interface, dependency in mapper.items():
        app.dependency_overrides[interface] = dependency
        
def build_dependencies() -> list:
    dependencies = []
    if settings.enable_limiter:
        dependencies.append(
            Depends(
                RateLimiter(
                    times=settings.rate_limit_requests_per_interval,
                    seconds=settings.requests_interval,
                )
            )
        )
    return dependencies