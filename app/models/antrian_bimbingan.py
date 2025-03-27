from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.config import Base
from datetime import datetime

class AntrianBimbingan(Base):
    __tablename__ = "antrian_bimbingan"

    id_antrian = Column(Integer, primary_key=True, index=True)
    nim = Column(String, ForeignKey("mahasiswa.nim"), nullable=False)
    nomor_induk = Column(String, ForeignKey("dosen.nomor_induk"), nullable=False)
    status_antrian = Column(String, nullable=False, default="Menunggu")
    waktu_antrian = Column(TIMESTAMP, nullable=False)
    # created_at = Column(DateTime, default=datetime.now(), nullable=False)
    # update_at = Column(DateTime, onupdate=datetime.now(), nullable=False)

    # mahasiswa = relationship("Mahasiswa", back_populates="antrian_bimbingan")
    # dosen = relationship("Dosen", back_populates="antrian_bimbingan")
