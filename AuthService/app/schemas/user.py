from uuid import UUID
from pydantic import BaseModel, EmailStr
from datetime import datetime

from schemas.role import RoleBase
from schemas.base import IdentifiableMixin

class UserBase(IdentifiableMixin):
    login: str
    email: EmailStr | None = None
    tg_id: str | None = None

class UserDTO(UserBase):
    roles: list[RoleBase] | None = None
    
class UserCreateDTO(BaseModel):
    login: str
    password: str
    email: EmailStr | None = None
    tg_id: str | None = None

class UserUpdateDTO(BaseModel):
    login: str | None = None
    email: EmailStr | None = None
    tg_id: str | None = None
    
class UserUpdatePasswordDTO(BaseModel):
    old_password: str
    new_password: str
    
class UserHistoryDTO(IdentifiableMixin):
    user_id: UUID
    attempted: datetime
    user_agent: str
    user_device_type: str
    success: bool
    
class UserHistoryCreateDTO(BaseModel):
    user_id: UUID
    user_agent: str
    user_device_type: str
    success: bool 
    attempted: datetime = datetime.now()
