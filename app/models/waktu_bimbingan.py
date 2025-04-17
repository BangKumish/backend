from sqlalchemy import Column, String, Integer, ForeignKey, Date, Time, DateTime
from sqlalchemy.orm import relationship

from app.config import Base

class WaktuBimbingan(Base):
    __tablename__ = "waktu_bimbingan"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nim = Column(String, ForeignKey('mahasiswa.nim'), nullable=False)
    nomor_induk = Column(String, ForeignKey('dosen.alias'), nullable=False)
    tanggal = Column(Date, nullable=False)
    waktu_mulai = Column(Time, nullable=False)
    waktu_selesai = Column(Time, nullable=False)
    
    # created_at = Column(DateTime, default=datetime.now(), nullable=False)
    # update_at = Column(DateTime, onupdate=datetime.now(), nullable=False)

    mahasiswa = relationship("Mahasiswa", back_populates="waktu_bimbingan")
    dosen = relationship("Dosen", back_populates="waktu_bimbingan")