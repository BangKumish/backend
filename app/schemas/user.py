from pydantic import BaseModel, EmailStr, ConfigDict, HttpUrl
from typing import Literal, Optional
from datetime import datetime
from uuid import UUID

class UserBase(BaseModel):
    email: EmailStr
    role: Literal["admin", "dosen", "mahasiswa"]

    model_config = ConfigDict(from_attributes=True)

class RegisterUser(UserBase):
    password: str
    full_name: Optional[str] = None

class LoginUser(BaseModel):
    email: EmailStr
    password: str

class UpdateProfile(BaseModel):
    full_name: Optional[str]
    avatar_utl: Optional[HttpUrl]
    ktm_url: Optional[HttpUrl]

    model_config = ConfigDict(from_attributes=True)

class AuthResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    role: str

class UserResponse(UserBase):
    id: UUID
    email: EmailStr
    role: str
    full_name: Optional[str]
    avatar_url: Optional[str]
    ktm_url: Optional[str]
    is_active: bool
    email_verified: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)