from pydantic import BaseModel
from typing import List
from typing import Optional
from app.schemas.file import FileSchema
# from datetime import datetime

class AntrianBimbinganSchema(BaseModel):
    nim: str
    nomor_induk: str
    waktu_id: int
    status_antrian: Optional[str] = "Menunggu"
    files: Optional[List[FileSchema]] = None
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
    file: Optional[FileSchema] = None
    
class UpdateAntrianSchema(BaseModel):
    status: Optional[str]