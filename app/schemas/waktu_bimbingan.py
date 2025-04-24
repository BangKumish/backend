from pydantic import BaseModel
from pydantic import ConfigDict

from typing import Optional
from datetime import date, time

class WaktuBimbinganSchema(BaseModel):
    id: int
    nomor_induk: str
    jumlah_antrian: int
    tanggal: date
    waktu_mulai: time
    waktu_selesai: time

    model_config = ConfigDict(from_attributes=True)

class UpdateWaktuBimbinganScheme(BaseModel):
    jumlah_antrian: Optional[int] = None
    tanggal: Optional[date] = None
    waktu_mulai: Optional[time] = None
    waktu_selesai: Optional[time] = None