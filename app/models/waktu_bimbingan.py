from sqlalchemy import Column, String, Integer, ForeignKey, Date, Time, DateTime
from sqlalchemy.orm import relationship

from app.config import Base

class WaktuBimbingan(Base):
    __tablename__ = "waktu_bimbingan"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nomor_induk = Column(String, ForeignKey('dosen.alias'), nullable=False)
    jumlah_antrian = Column(Integer, nullable=False, default=5)
    tanggal = Column(Date, nullable=False)
    waktu_mulai = Column(Time, nullable=False)
    waktu_selesai = Column(Time, nullable=False)
    
    # created_at = Column(DateTime, default=datetime.now(), nullable=False)
    # update_at = Column(DateTime, onupdate=datetime.now(), nullable=False)

    dosen = relationship("Dosen", back_populates="waktu_bimbingan")
    antrian_bimbingan = relationship("AntrianBimbingan", back_populates="waktu_bimbingan")