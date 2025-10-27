from pydantic import BaseModel, EmailStr
from typing import Optional

#Schema for reading user data
class UserBase(BaseModel):
    name: str
    email: Optional[EmailStr] = None

#Schema for creating users
class UserCreate(UserBase):
    pass #This will inherit name and email from UserBase


#Schema for reading user with ID (responsee)
class User(UserBase):
    id: int

    class Config:
        from_attributes = True # Will allow returning SQLAlchemy models directly #Pydantic v1 takes orm_mode and v2 takes from_attributes