from enum import Enum
from uuid import UUID

from pydantic import BaseModel, EmailStr

class SocialNetworks(Enum):
    VK = 'vk'
    YANDEX = 'yandex'
    
class SocialUser(BaseModel):
    id: str
    login: str
    social_name: SocialNetworks
    email: EmailStr | None = None
    tg_id: str | None = None
    
class SocialCreateDTO(BaseModel):
    user_id: UUID
    social_id: str
    social_name: SocialNetworks