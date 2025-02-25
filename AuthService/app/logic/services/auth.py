from abc import ABC, abstractmethod
from dataclasses import dataclass
from functools import wraps
from typing import Any
from datetime import UTC, datetime
from time import time

import async_fastapi_jwt_auth
from async_fastapi_jwt_auth import AuthJWT
from async_fastapi_jwt_auth.exceptions import JWTDecodeError, MissingTokenError
from fastapi import HTTPException, status

from schemas.user import UserHistoryCreateDTO
from logic.services.user import BaseUserService
from infrastructure.storages.token import TokenStorage
from infrastructure.models.user import User
from schemas.result import Error, GenericResult
from schemas.token import Token, TokenJTI


@dataclass
class BaseAuthService(ABC):
    @abstractmethod
    async def login(
        self, login: str, password: str, user_agent: str
    ) -> GenericResult[Token]:
        ...
        
    @abstractmethod
    async def login_by_oauth(self, *, login: str) -> GenericResult[Token]:
        ...
    
    @abstractmethod
    async def logout(self):
        ...
        
    @abstractmethod
    async def refresh(self, access_jti: str | None) -> Token:
        ...
        
    @abstractmethod
    async def require_auth(self):
        ...
        
    @abstractmethod
    async def optional_auth(self):
        ...
        
    @abstractmethod
    async def get_user(self) -> User | None:
        ...
        
    @abstractmethod
    async def get_auth_user(self, token: str) -> User | None:
        ...
        
        
@dataclass 
class AuthService(BaseAuthService):
    _auth_jwt_service: AuthJWT
    _token_storage: TokenStorage
    _user_service: BaseUserService
    
    async def _generate_token(self, user_id: Any) -> Token:
        return Token(
            access_token = await self._auth_jwt_service.
                create_access_token(subject=user_id),
            refresh_token= await self._auth_jwt_service.
                create_refresh_token(subject=user_id)
        )
    
    async def _get_jti(self) -> str:
        return (await self._auth_jwt_service.get_raw_jwt())["jti"]
    
    async def _check_token_expiracy(self) -> bool:
        jti = await self._get_jti()
        return await self._token_storage.check_expiration(jti=jti)
    
    async def _refresh_token_required(self):
        try:
            await self._auth_jwt_service.jwt_refresh_token_required()
            if self._check_token_expiracy():
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED, detail="Unathorized"
                )
        except JWTDecodeError as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detai=e.message
            )
        except MissingTokenError as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail=e.message
            )
    
    async def _decode_token(self, token: str):
        try:
            return await self._auth_jwt_service.get_raw_jwt(token)
        except JWTDecodeError as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail=e.message
            )
            
    async def login(
        self, login: str, password: str, user_agent: str
    ) -> GenericResult[Token]:
        user = await self._user_service.get_user_by_login(login=login)
        if not user or not user.check_password(password=password):
            return GenericResult.failure(
                Error(
                    error_code="WRONG_LOGIN_OR_PASSWORD",
                    reason="Wrong login or password"
                )
            )
        user_history = UserHistoryCreateDTO(
            user_id=user.id,
            attempted=datetime.now(UTC),
            user_agent=user_agent,
            user_device_type="web",
            success=True
        )
        await self._user_service.insert_user_login(
            user_id=user.id, history_row=user_history
        )
        tokens = await self._generate_token(user_id=str(user.id))
        await self._auth_jwt_service.set_access_cookies(tokens.access_token)
        await self._auth_jwt_service.set_refresh_cookies(tokens.refresh_token)
        return GenericResult.success(tokens)
    
    async def login_by_oauth(self, *, login: str) -> GenericResult[Token]:
        user = await self._user_service.get_user_by_login(login=login)
        if not user:
            return GenericResult.failure(
                error=Error(
                    error_code="WRONG_LOGIN_OR_PASSWORD",
                    reason="Wrong login or password"
                )
            )
        user_history = UserHistoryCreateDTO(
            user_id=user.id,
            attempted=datetime.now(UTC),
            user_agent="oauth2",
            user_device_type="web",
            success=True
        )
        await self._user_service.insert_user_login(
            user_id=user.id, history_row=user_history
        )    
        
        tokens = await self._generate_token(user_id=str(user.id))
        await self._auth_jwt_service.set_access_cookies(tokens.access_token)
        await self._auth_jwt_service.set_refresh_cookies(tokens.refresh_token)
        return GenericResult.success(tokens)    
    
    async def logout(self) -> None:
        await self.require_auth()
        access_jti = (await self._auth_jwt_service.get_raw_jwt())["jti"]
        # await self._auth_jwt_service.unset_jwt_cookies()
        await self._auth_jwt_service.unset_access_cookies()
        await self._auth_jwt_service.unset_refresh_cookies()
        token_jti = TokenJTI(
            access_token_jti=access_jti,
            refresh_token_jti=None
        )
        return await self._token_storage.store_token(token=token_jti)
    
    async def refresh(self, access_jti: str) -> Token:
        await self._refresh_token_required()
        refresh_jti = await self._get_jti()
        token_jti = TokenJTI(
            access_token_jti=access_jti,
            refresh_token_jti=refresh_jti
        )
        await self._token_storage.store_token(token_jti=token_jti)
        user_subject = await self._auth_jwt_service.get_jwt_subject()
        tokens = await self._generate_token(user_id=user_subject)
        await self._auth_jwt_service.set_access_cookies(tokens.access_token)
        await self._auth_jwt_service.set_refresh_cookies(tokens.refresh_token)
        return tokens
    
    async def require_auth(self):
        try: 
            await self._auth_jwt_service.jwt_required()
            if await self._check_token_expiracy():
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED, detail="Unathorized"
                )
        except JWTDecodeError as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail=e.message
            )
        except MissingTokenError as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail=e.message
            )
        
    async def optional_auth(self):
        return await self._auth_jwt_service.jwt_optional()
    
    async def get_user(self) -> User | None:
        await self.require_auth()
        user_subject = await self._auth_jwt_service.get_jwt_subject()
        user: GenericResult[User] = await self._user_service.get_user(
            user_id=user_subject
        )
        return user.response
    
    async def get_auth_user(self, access_token: str) -> User | None:
        decoded = await self._decode_token(access_token)
        if decoded["exp"] <= time():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is expired"
            )
        user_id = decoded["sub"]
        user = await self._user_service.get_user(id=user_id)
        return user.response
    
        
def require_roles(roles: list[str]):
    def auth_decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            auth_service = kwargs["auth_service"]
            current_user: User = await auth_service.get_user()
            if not current_user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized"
                )
            for role in current_user.roles:
                if role.name in roles:
                    return await func(*args, **kwargs)
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="User have not access"
            )

        return wrapper

    return auth_decorator 