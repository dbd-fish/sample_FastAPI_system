from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from uuid import UUID



class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class PasswordReset(BaseModel):
    email: EmailStr
    new_password: str

class UserResponse(BaseModel):
    user_id: UUID
    username: str
    email: str
    contact_number: Optional[str]
    date_of_birth: Optional[datetime]
    user_role: int
    user_status: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes  = True
