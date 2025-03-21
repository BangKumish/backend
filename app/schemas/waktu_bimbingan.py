from pydantic import BaseModel
from datetime import date, time

class WaktuBimbinganSchema(BaseModel):
    nomor_induk: str
    nim: str
    tanggal: date
    waktu_mulai: time
    waktu_selesai: time