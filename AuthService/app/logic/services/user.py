from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, List

from faker import Faker

from schemas.events import UserRegisteredEventDTO
from infrastructure.kafka.sender import KafkaSender, get_producer
from logic.dependencies.services.sender_factory import create_sender
from infrastructure.models.social_account import SocialAccount
from logic.unit_of_work.base import BaseUnitOfWork
from infrastructure.repositories.user import BaseUserRepository
from infrastructure.models.user import User
from infrastructure.models.user_history import UserHistory
from schemas.result import Error, GenericResult
from schemas.social import SocialUser
from schemas.user import UserCreateDTO, UserHistoryCreateDTO, UserUpdateDTO, UserUpdatePasswordDTO


@dataclass
class BaseUserService(ABC):
    @abstractmethod
    async def get_user_history(
        self, *, user_id: Any, skip: int, limit: int
    ) -> list[UserHistory]:
        ...

    @abstractmethod
    async def get_users(self, *, skip: int, limit: int) -> list[User]:
        ...

    @abstractmethod
    async def update_password(
        self, *, user_id: Any, password_user: UserUpdatePasswordDTO
    ) -> GenericResult[User]:
        ...

    @abstractmethod
    async def create_user(self, user_dto: UserCreateDTO) -> GenericResult[User]:
        ...

    @abstractmethod
    async def insert_user_login(
        self, *, user_id: Any, history_row: UserHistoryCreateDTO
    ):
        ...

    @abstractmethod
    async def get_user(self, *, user_id: Any) -> GenericResult[User]:
        ...

    @abstractmethod
    async def get_user_by_login(self, *, login: str) -> User | None:
        ...

    @abstractmethod
    async def get_or_create_user(self, *, social: SocialUser) -> GenericResult[User]:
        ...

    @abstractmethod
    async def update_user(
        self, user_id: Any, user_dto: UserUpdateDTO
    ) -> GenericResult[User]:
        ...

    @abstractmethod
    async def delete_user(self, *, user_id: Any) -> None:
        ...
        

@dataclass
class UserService(BaseUserService):
    _repository: BaseUserRepository
    _uow: BaseUnitOfWork
    
    async def get_user_history(self, *, user_id: Any, skip: int = 0, limit: int = 100) -> List[UserHistory]:
        return await self._repository.get_user_history(
            user_id=user_id, skip=skip, limit=limit
        )
        
    async def get_users(self, *, skip : int = 0, limit: int=100) -> List[User]:
        return await self._repository.gets(skip=skip, limit=limit)
    
    async def update_password(
        self, *, user_id: Any, password_user: UserUpdatePasswordDTO
    ) -> GenericResult[User]:
        user: User = await self._repository.get(id=user_id)
        if not user:
            return GenericResult.failure(
                Error(error_code="USER_NOT_FOUND", reason="User not found"),
            )
        status= user.change_password(
            old_password=password_user.old_password,
            new_password=password_user.new_password
        )
        if status:
            await self._uow.commit()
        return GenericResult.success(user)
    
    async def create_user(self, user_dto: UserCreateDTO) -> GenericResult[User]:
        user = await self._repository.get_by_login(login=user_dto.login)
        response = GenericResult.failure(
            Error(error_code="USER_ALREADY_EXISTS", reason="User already exists")
        )
        if not user:
            user = await self._repository.insert(body=user_dto)
            await self._uow.commit()
            response = GenericResult.success(user)
            sender : KafkaSender = create_sender(get_producer())
            await sender.send_on_register(
                UserRegisteredEventDTO(
                    user_login=user_dto.login,
                    user_email=user_dto.email)
            )
            
            
            
            
        return response
    
    async def insert_user_login(
        self, *, user_id: Any, history_row: UserHistoryCreateDTO
    ) -> GenericResult[UserHistory]:
        result = await self._repository.insert_user_login(
            user_id=user_id, data=history_row
        )
        if result.is_success:
            await self._uow.commit()
        return result
    
    async def get_user(self, *, user_id: Any) -> GenericResult[User]:
        user = await self._repository.get(id=user_id)
        if not user:
            return GenericResult.failure(
                Error(error_code="USER_NOT_FOUND", reason="User not found")
            )
        return GenericResult.success(user)
    
    async def get_user_by_login(self, *, login: str) -> User | None:
        return await self._repository.get_by_login(login=login)
    
    async def get_or_create_user(self, *, social: SocialUser) -> GenericResult[User]:
        social_user = await self._repository.get_user_social(
            social_id=social.id, social_name=social.social_name
        )
        if not social_user:
            auto_password  = Faker().password()
            user = await self.get_user_by_login(login=social.login)
            if user:
                return GenericResult.failure(
                    Error(error_code="USER_ALREADY_EXISTS", reason="User already exists")
                )
            user_dto = UserCreateDTO(
                login=social.login,
                password=auto_password,
                email=social.email
            )
            user = await self._repository.insert(body=user_dto)
            user.add_social_account(
                social_account=SocialAccount(
                    user_id=user.id,
                    social_id=social.id,
                    social_name=social.social_name
                )
            )
            await self._uow.commit()
            return GenericResult.success(user)
        return await self.get_user(user_id=social_user.user_id)
    
    async def update_user(
        self, user_id: Any, user_dto: UserUpdateDTO
    ) -> GenericResult[User]:
        user = await self._repository.get(id=user_id)
        if not user:
            return GenericResult.failure(
                Error(
                    error_code="USER_NOT_FOUND",
                    reason="User not found"
                )
            )
        user.update_personal(**user_dto.model_dump())
        await self._uow.commit()
        return GenericResult.success(user)
    
    async def delete_user(self, *, user_id) -> None:
       await self._repository.delete(id=user_id)
       return await self._uow.commit()
   
    def __hash__(self):
        return hash((self._repository, self._uow))
        
    def __eq__(self, other):
        return hash(self) == hash(other)