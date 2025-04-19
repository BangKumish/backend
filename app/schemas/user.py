from pydantic import BaseModel, EmailStr
from typing import Optional, Literal

class RegisterUser(BaseModel):
    email: EmailStr
    password: str
    name: str
    role: Literal["admin, dosen, mahasiswa"]
    alias: Optional[str] = None
    nim: Optional[str] = None

class LoginUser(BaseModel):
    email: EmailStr
    password: str

class AuthResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"