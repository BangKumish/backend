from pydantic import BaseModel
from datetime import datetime

class AntrianBimbinganSchema(BaseModel):
    nim: str
    nomor_induk: str
    status_antrian: str = "Menunggu"
    waktu_antrian: datetime
