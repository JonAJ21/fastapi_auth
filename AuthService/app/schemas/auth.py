from pydantic import BaseModel

class UserLoginDTO(BaseModel):
    login: str
    password: str

class RefreshRequestDTO(BaseModel):
    jti: str | None