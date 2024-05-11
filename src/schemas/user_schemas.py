from typing import Optional
from pydantic import BaseModel, EmailStr


class UserSchema(BaseModel):
    id: Optional[int] = None
    name: str
    email: EmailStr

    class Config:
        from_attributes = True


class UserCreateSchema(UserSchema):
    name: str
    email: EmailStr
    password: str


class LoginSchema(BaseModel):
    email: EmailStr
    password: str

    class Config:
        from_attributes = True
