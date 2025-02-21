from pydantic import BaseModel

class Token(BaseModel):
    access_token: str | None
    refresh_token: str | None
    
class TokenJTI(BaseModel):
    access_token_jti: str | None
    refresh_token_jti: str | None
    
class TokenValidaton(BaseModel):
    access_token: str