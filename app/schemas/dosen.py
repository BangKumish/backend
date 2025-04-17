from pydantic import BaseModel
from typing import Optional

class DosenSchema(BaseModel):
    nomor_induk: str
    name: str
    alias: str
    email: str
    password: str
    status_kehadiran: str
    ketersediaan_bimbingan: bool = True
    class Config:
        from_attributes = True

class DosenUpdateSchema(BaseModel):
    nomor_induk: Optional[str] = None
    name: Optional[str] = None
    alias: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    status_kehadiran: Optional[str] = None
    ketersediaan_bimbingan: Optional[bool] = None
    jumlah_bimbingan: Optional[int] = None