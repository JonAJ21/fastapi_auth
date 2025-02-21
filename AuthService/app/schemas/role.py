from pydantic import BaseModel
from enum import Enum

from schemas.base import IdentifiableMixin

class RoleBase(IdentifiableMixin):
    name: str
    description: str | None = None

class RoleDTO(RoleBase):
    ...

class RoleCreateDTO(BaseModel):
    name: str
    description: str | None = None
    
class RoleUpdateDTO(RoleBase):
    name: str
    description: str | None = None
    
class Roles(Enum):
    SUPER_ADMIN = 'super_admin'
    ADMIN = 'admin'
    USER = 'user'