from sqlalchemy import Column, String, ForeignKey, Integer, UniqueConstraint, DateTime
from sqlalchemy.orm import relationship, validates
from app.config import Base

from datetime import datetime
class MahasiswaDosen(Base):
    __tablename__ = "mahasiswa_dosen"

    id = Column(Integer, primary_key=True, autoincrement=True)
    mahasiswa_nim = Column(String, ForeignKey("mahasiswa.nim"), nullable=False)
    dosen_alias = Column(String, ForeignKey("dosen.alias"))
    role = Column(String)
    created_at = Column(DateTime, default=datetime.now(), nullable=False)
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now(), nullable=False)

    mahasiswa = relationship("Mahasiswa", back_populates="dosen_relation")
    dosen = relationship("Dosen", back_populates="mahasiswa_relation")
    
    __table_args__ = (
        UniqueConstraint("mahasiswa_nim", "dosen_alias", "role", name="unique_mahasiswa_dosen_role"),
    )