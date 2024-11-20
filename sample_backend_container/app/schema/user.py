from pydantic import BaseModel, EmailStr
from uuid import UUID

class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str

class PasswordReset(BaseModel):
    email: EmailStr
    new_password: str

class UserResponse(BaseModel):
    user_id: UUID
    email: EmailStr
    username: str

    class Config:
        from_attributes = True
