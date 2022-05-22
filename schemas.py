from datetime import datetime
from pydantic import BaseModel, EmailStr

class SignUpPayload(BaseModel):
    name: str
    email: EmailStr
    password: str

class SignInPayload(BaseModel):
    email: EmailStr
    password: str

class UserSchema(BaseModel):
    id: str
    name: str
    email: EmailStr
    password_hash: str

    class Config:
        orm_mode = True

class ReturnToken(BaseModel):
    token: str

class ContentPayload(BaseModel):
    content: str

class ContentSchema(BaseModel):
    id: str
    content: str
    user: UserSchema
    created_at: datetime

    class Config:
        orm_mode = True
