from pydantic import BaseModel
from typing import Optional
# from datetime import datetime

class AntrianBimbinganSchema(BaseModel):
    nim: str
    nomor_induk: str
    waktu_id: int
    status_antrian: Optional[str] = "Menunggu"
    # waktu_antrian: datetime

    class Config:
        from_attributes = True

class AmbilAntrianSchema(BaseModel):
    nim: str
    waktu_id: int

class AmbilAntrianResponse(BaseModel):
    message: str
    posisi: int
    antrian_id: int
    antrian: AmbilAntrianSchema
    
class UpdateAntrianSchema(BaseModel):
    status: Optional[str]