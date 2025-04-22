from pydantic import BaseModel
from typing import Optional
from uuid import UUID

class MahasiswaSchema(BaseModel):
    id: UUID
    nim: str
    nama: str
    email: str
    password: str
    topik_penelitian: str

    class Config:
        from_attributes = True

class MahasiswaUpdateSchema(BaseModel):
    nim: Optional[str] = None
    nama: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    topik_penelitian: Optional[str] = None

class MahasiswaCreateSchema(BaseModel):
    nim: str
    nama: str
    email: str

class MahasiswaResponseSchema(BaseModel):
    nim: str
    nama: str
    email: str
    password: str