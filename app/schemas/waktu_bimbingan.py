from pydantic import BaseModel
from pydantic import ConfigDict

from typing import Optional
from typing import List

from datetime import date, time

from app.schemas.antrian_bimbingan import AntrianBimbinganSchema

class WaktuBimbinganSchema(BaseModel):
    id: int
    nomor_induk: str
    jumlah_antrian: int
    tanggal: date
    waktu_mulai: time
    waktu_selesai: time
    antrian_bimbingan: List[AntrianBimbinganSchema] = []

    model_config = ConfigDict(from_attributes=True)

class CreateWaktuBimbinganScheme(BaseModel):
    nomor_induk: str
    jumlah_antrian: int
    tanggal: date
    waktu_mulai: time
    waktu_selesai: time

class UpdateWaktuBimbinganScheme(BaseModel):
    jumlah_antrian: Optional[int] = None
    tanggal: Optional[date] = None
    waktu_mulai: Optional[time] = None
    waktu_selesai: Optional[time] = None