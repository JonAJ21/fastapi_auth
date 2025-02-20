from pydantic import BaseModel
from enum import Enum

from schemas.base import IdentifiableMixin

class RoleBase(IdentifiableMixin):
    name: str
    description: str

class RoleDTO(RoleBase):
    ...

class RoleCreateDTO(BaseModel):
    name: str
    description: str | None
    
class RoleUpdateDTO(RoleBase):
    name: str
    description: str | None
    
class Roles(Enum):
    SUPER_ADMIN = 'super_admin'
    ADMIN = 'admin'
    USER = 'user'