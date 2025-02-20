from abc import abstractmethod
from dataclasses import dataclass
from typing import Any, List

from sqlalchemy import and_, select
from sqlalchemy.orm import noload, selectinload

from logic.services.cache import BaseCacheService
from schemas.social import SocialCreateDTO
from schemas.result import GenericResult, ModelType
from schemas.user import UserCreateDTO, UserHistoryCreateDTO
from infrastructure.models.social_account import SocialAccount, SocialNetworks
from infrastructure.models.user_history import UserHistory
from infrastructure.models.user import User
from infrastructure.repositories.base import BaseRepository
from infrastructure.repositories.cache import CacheRepository
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
class UserRepository(PostgresRepository[User, UserCreateDTO], BaseUserRepository):
    _model = User
    
    async def get_by_login(self, *, login: str) -> User:
        statement = select(self._model).where(self._model.login == login)
        return await self._session.execute(statement).scalar_one_or_none() 
    
    async def get(self, *, id: Any) -> ModelType | None:
        statement = (
            select(self._model)
            .options(noload(self._model.history))
            .options(selectinload(self._model.roles))
            .where(self._model.id == id)
        )
        return await self._session.execute(statement).scalar_one_or_none()
    
    async def get_user_history(
        self, *, user_id: Any, skip: int, limit: int
    ) -> List[UserHistory]:
        statement = (
            select(UserHistory)
            .where(UserHistory.user_id == user_id)
            .order_by()
            .offset(skip)
            .limit(limit)
        )
        return await self._session.execute(statement).scalars().all()
    
    async def get_user_social(
        self, *, social_id: str, social_name: SocialNetworks
    ) -> SocialAccount | None:
        statement = (
            select(SocialAccount)
            .where(
                and_(
                    SocialAccount.social_network == social_name,
                    SocialAccount.social_id == social_id
                )
            )
        )
        return await self._session.execute(statement).scalar_one_or_none()
    
    async def insert_user_login(
        self, *, user_id: Any, data: UserHistoryCreateDTO
    ) -> GenericResult[UserHistory]:
        user: User = await self.get(id=user_id)
        if not user:
            GenericResult.failure(
                error_code="USER_NOT_FOUND",
                reason="User not found"
            )
        user_history = UserHistory(**data.model_dump())
        user.add_user_session(user_history)
        return GenericResult.success(user)
    
    async def insert_user_social(
        self, *, user_id: Any, data: SocialCreateDTO
    ) -> GenericResult[SocialAccount]:
        user: User = await self.get(id=user_id)
        if not user:
            GenericResult.failure(
                error_code="USER_NOT_FOUND",
                reason="User not found"
            )
        social = SocialAccount(**data.model_dump())
        user.add_social_account(social)
        return GenericResult.success(social)
    
@dataclass
class CacheUserRepository(
    CacheRepository[User, UserCreateDTO], BaseUserRepository
):
    _repository: BaseUserRepository
    _cache_service: BaseCacheService
    
    async def get_by_login(self, *, login: str) -> User:
        key = f"{self._model.__name__}_{login}"
        entity = await self._cache_service.get(key=key)
        if not entity:
            entity = await self._repository.get_by_login(login=login)
        return entity
    
    async def get_user_history(
        self, *, user_id: Any, skip: int, limit: int
    ) -> List[UserHistory]:
        return await self._repository.get_user_history(
            user_id=user_id, skip=skip, limit=limit
        )
    
    async def get_user_social(
        self, *, social_id: str, social_name: SocialNetworks
    ) -> SocialAccount | None:
        return await self._repository.get_user_social(
            social_id=social_id, social_name=social_name
        )
        
    async def insert_user_login(
        self, *, user_id: Any, data: UserHistoryCreateDTO
    ) -> GenericResult[UserHistory]:
        return await self._repository.insert_user_login(
            user_id=user_id, data=data
        )
        
    async def insert_user_social(
        self, *, user_id: Any, data: SocialCreateDTO
    ) -> GenericResult[SocialAccount]:
        return await self._repository.insert_user_social(
            user_id=user_id, data=data
        )