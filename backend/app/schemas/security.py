from typing import Optional

from pydantic import BaseModel

class Message(BaseModel):
    message: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenPayload(BaseModel):
    sub: Optional[int]

class NewPassword(BaseModel):
    token: str
    new_password: str
