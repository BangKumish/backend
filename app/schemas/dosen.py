from pydantic import BaseModel
from app.schemas.waktu_bimbingan import WaktuBimbinganSchema

class DosenSchema(BaseModel):
    nomor_induk: str
    name: str
    email: str
    password: str
    status_kehadiran: str
    ketersediaan_bimbingan: bool = True
    jumlah_bimbingan: int = 0
    # waktu_bimbingan: list[WaktuBimbinganSchema]

    class Config:
        from_attributes = True