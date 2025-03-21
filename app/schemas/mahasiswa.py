from pydantic import BaseModel

class MahasiswaSchema(BaseModel):
    nim: str
    nama: str
    email: str
    password: str
    topik_penelitian: str

    class Config:
        from_attributes = True