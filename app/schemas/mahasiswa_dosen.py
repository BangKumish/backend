from pydantic import BaseModel

class MahasiswaDosenSchema(BaseModel):
    id: int
    mahasiswa_nim: str
    dosen_id: str
    role: str
