from abc import abstractmethod
from dataclasses import dataclass
from typing import Any, List, Type

from sqlalchemy import and_, select
from sqlalchemy.orm import noload, selectinload

from logic.services.cache import BaseCacheService
from schemas.social import SocialCreateDTO
from schemas.result import Error, GenericResult, ModelType
from schemas.user import UserCreateDTO, UserHistoryCreateDTO
from infrastructure.models.social_account import SocialAccount, SocialNetworks
from infrastructure.models.user_history import UserHistory
from infrastructure.models.user import User
from infrastructure.repositories.base import BaseRepository
from infrastructure.repositories.cache import PostgresCacheRepository
from infrastructure.repositories.postgre import PostgresRepository


@dataclass
class BaseUserRepository(BaseRepository):
    @abstractmethod
    async def get_by_login(self, *, login: str) -> User:
        ...
        
    @abstractmethod
    async def get_user_history(
        self, *, user_id: Any, skip: int = 0, limit: int
    ) -> List[UserHistory]:
        ...
        
    @abstractmethod
    async def get_user_social(
        self, *, social_id: str, social_name: SocialNetworks
    ) -> SocialAccount:
        ...
        
    @abstractmethod
    async def insert_user_login(
        self, *, user_id: Any, data: UserHistoryCreateDTO
    ) -> GenericResult[UserHistory]:
        ...
        
    @abstractmethod
    async def insert_user_social(
        self, *, user_id: Any, data: SocialCreateDTO
    ) -> GenericResult[SocialAccount]:
        ...
        

@dataclass
class PostgresUserRepository(PostgresRepository[User, UserCreateDTO], BaseUserRepository):
    _model: Type[ModelType] = User
    
    async def get_by_login(self, *, login: str) -> User:
        statement = select(self._model).where(self._model.login == login)
        return (await self._session.execute(statement)).scalar_one_or_none() 
    
    async def get(self, *, id: Any) -> ModelType | None:
        statement = (
            select(self._model)
            .options(noload(self._model.history))
            .options(selectinload(self._model.roles))
            .where(self._model.id == id)
        )
        return (await self._session.execute(statement)).scalar_one_or_none()
    
    async def get_user_history(
        self, *, user_id: Any, skip: int = 0, limit: int = 100
    ) -> List[UserHistory]:
        statement = (
            select(UserHistory)
            .where(UserHistory.user_id == user_id)
            .order_by()
            .offset(skip)
            .limit(limit)
        )
        return (await self._session.execute(statement)).scalars().all()
    
    async def get_user_social(
        self, *, social_id: str, social_name: SocialNetworks
    ) -> SocialAccount | None:
        statement = (
            select(SocialAccount)
            .where(
                and_(
                    SocialAccount.social_name == social_name,
                    SocialAccount.social_id == social_id
                )
            )
        )
        return (await self._session.execute(statement)).scalar_one_or_none()
    
    async def insert_user_login(
        self, *, user_id: Any, data: UserHistoryCreateDTO
    ) -> GenericResult[UserHistory]:
        user: User = await self.get(id=user_id)
        if not user:
            return GenericResult.failure(
                error=Error(error_code="USER_NOT_FOUND", reason="User not found"),
            )
        user_history = UserHistory(**data.model_dump())
        user.add_user_session(user_history)
        return GenericResult.success(user_history)
    
    async def insert_user_social(
        self, *, user_id: Any, data: SocialCreateDTO
    ) -> GenericResult[SocialAccount]:
        user: User = await self.get(id=user_id)
        if not user:
            return GenericResult.failure(
                error=Error(error_code="USER_NOT_FOUND", reason="User not found"),
            )
        social = SocialAccount(**data.model_dump())
        user.add_social_account(social)
        return GenericResult.success(social)
    
    def __hash__(self):
        return hash((self._model))
        
    def __eq__(self, other):
        return hash(self) == hash(other)
    
@dataclass
class PostgresCacheUserRepository(
    PostgresCacheRepository[User, UserCreateDTO], PostgresUserRepository
):
    _cache_service: BaseCacheService | None = None
    _model: Type[ModelType] = User
    
    async def get_by_login(self, *, login: str) -> User:
        key = f"{self._model.__name__}_{login}"
        if self._cache_service is not None:
            entity = await self._cache_service.get(key=key)
        if not entity:
            entity = await super().get_by_login(login=login)
        return entity
    
    async def get_user_history(
        self, *, user_id: Any, skip: int = 0, limit: int = 100
    ) -> List[UserHistory]:
        return await super().get_user_history(
            user_id=user_id, skip=skip, limit=limit
        )
    
    async def get_user_social(
        self, *, social_id: str, social_name: SocialNetworks
    ) -> SocialAccount | None:
        return await super().get_user_social(
            social_id=social_id, social_name=social_name
        )
        
    async def insert_user_login(
        self, *, user_id: Any, data: UserHistoryCreateDTO
    ) -> GenericResult[UserHistory]:
        return await super().insert_user_login(
            user_id=user_id, data=data
        )
        
    async def insert_user_social(
        self, *, user_id: Any, data: SocialCreateDTO
    ) -> GenericResult[SocialAccount]:
        return await super().insert_user_social(
            user_id=user_id, data=data
        )
        
    def __hash__(self):
        return hash((self._model, self._cache_service))
        
    def __eq__(self, other):
        return hash(self) == hash(other)