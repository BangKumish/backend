from pydantic import BaseModel
from typing import Optional

class MahasiswaDosenSchema(BaseModel):
    id: int
    mahasiswa_nim: str
    dosen_alias: str
    role: str
    
    class Config:
        from_attributes = True

class MahasiswaDosenCreateSchema(BaseModel):
    mahasiswa_nim: str
    dosen_alias: str
    role: str

class MahasiswaDosenUpdateSchema(BaseModel):
    role: Optional[str] = None