from pydantic import BaseModel
from datetime import date, time

class WaktuBimbinganSchema(BaseModel):
    id: int
    nomor_induk: str
    jumlah_antrian: int
    tanggal: date
    waktu_mulai: time
    waktu_selesai: time