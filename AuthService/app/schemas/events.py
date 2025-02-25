from pydantic import BaseModel, EmailStr


class UserRegisteredEventDTO(BaseModel):
    user_login: str
    user_email: EmailStr | None = None
    event: str = "User registered"