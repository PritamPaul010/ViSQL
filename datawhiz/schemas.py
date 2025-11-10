from pydantic import BaseModel, EmailStr
from typing import Optional

from datawhiz.models import RoleEnum


# Schema for reading user data
class UserBase(BaseModel):
    name: str
    email: Optional[EmailStr] = None

# Schema for creating users
class UserCreate(UserBase):
    # This will inherit name and email from UserBase
    password: str

# Schema for reading user with ID (responsee)
class User(UserBase):
    # This will inherit name and email from UserBase
    id: int
    role: RoleEnum

    class Config:
        from_attributes = True # Will allow returning SQLAlchemy models directly #Pydantic v1 takes orm_mode and v2 takes from_attributes


# Schema for User Login Request
class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token : str
    token_type : str = 'bearer'

class PasswordUpdateRequest(BaseModel):
    current_password: str
    new_password: str

# Schema for Basic Response
class MessageResponse(BaseModel):
    message: str


