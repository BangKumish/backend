from sqlalchemy import Column, String, Integer, ForeignKey, Date, Time
from sqlalchemy.orm import relationship

from app.config import Base

class WaktuBimbingan(Base):
    __tablename__ = "waktu_bimbingan"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nim = Column(String, ForeignKey('mahasiswa.nim'), nullable=False)
    nomor_induk = Column(String, ForeignKey('dosen.nomor_induk'), nullable=False)
    tanggal = Column(Date, nullable=False)
    waktu_mulai = Column(Time, nullable=False)
    waktu_selesai = Column(Time, nullable=False)

    mahasiswa = relationship("Mahasiswa", back_populates="waktu_bimbingan")
    dosen = relationship("Dosen", back_populates="waktu_bimbingan")