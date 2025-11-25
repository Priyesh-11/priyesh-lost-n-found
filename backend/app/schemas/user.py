from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr
    username: str
    full_name: Optional[str] = None
    phone: Optional[str] = None
    avatar_url: Optional[str] = None

class UserBasic(BaseModel):
    id: int
    username: str
    full_name: Optional[str] = None
    avatar_url: Optional[str] = None
    email: EmailStr # Included for contact info
    phone: Optional[str] = None # Included for contact info

    class Config:
        from_attributes = True

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    phone: Optional[str] = None
    avatar_url: Optional[str] = None
    password: Optional[str] = None

class UserInDBBase(UserBase):
    id: int
    role_id: int
    is_active: bool
    is_verified: bool
    reputation_score: int
    created_at: datetime

    class Config:
        from_attributes = True

class UserOut(UserInDBBase):
    pass

class UserInDB(UserInDBBase):
    hashed_password: str
