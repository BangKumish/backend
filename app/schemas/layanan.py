from pydantic import BaseModel

class LayananSchema(BaseModel):
    layanan_id: int
    layanan_jenis: str
    layanan_file: str
    layanan_status: int

    class Config:
        from_attributes = True