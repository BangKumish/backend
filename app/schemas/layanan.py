from pydantic import BaseModel
from typing import Optional
from uuid import UUID

from datetime import datetime

class LayananSchema(BaseModel):
    layanan_id: int
    layanan_jenis: str
    layanan_file: str
    layanan_status: int

    class Config:
        from_attributes = True

# ================================
# JENIS LAYANAN
# ================================
class JenisLayananBase(BaseModel):
    nama_layanan: str
    deskripsi: Optional[str] = None
    is_aktif: Optional[bool] = True
    url_file: Optional[str] = None

class JenisLayananCreate(JenisLayananBase):
    pass

class JenisLayananResponse (JenisLayananBase):
    id:int

    class Config:
        from_attributes = True



# ================================
#  DOKUMEN PERSYARATAN
# ================================

class DokumenPersyaratanBase(BaseModel):
    nama_dokumen: str
    is_wajib: Optional[bool] = True

class DokumenPersyaratanCreate(DokumenPersyaratanBase):
    jenis_layanan_id: int

class DokumenPersyaratanResponse(DokumenPersyaratanBase):
    id: int
    jenis_layanan_id: int

    class Config:
        from_attributes = True



# ================================
# PENGAJUAN LAYANAN
# ================================

class PengajuanLayananBase(BaseModel):
    mahasiswa_nim: str
    jenis_layanan_id: int
    status: Optional[str] = "Menunggu"
    catatan_admin: Optional[str] = None

class PengajuanLayananCreate(PengajuanLayananBase):
    pass

class PengajuanLayananResponse(PengajuanLayananBase):
    id: UUID
    created_at: datetime

    class Config:
        from_attributes = True



# ================================
# LAMPIRAN LAYANAN
# ================================

class LampiranPengajuanBase(BaseModel):
    nama_dokumen: str
    file_url: str

class LampiranPengajuanCreate(LampiranPengajuanBase):
    pengajuan_id: int

class LampiranPengajuanResponse(LampiranPengajuanBase):
    id: UUID
    pengajuan_id: UUID
    uploaded_at: datetime

    class Config:
        from_attributes = True