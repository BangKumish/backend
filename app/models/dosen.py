from typing import List

from sqlalchemy import Column, String, Integer, Boolean, DateTime
from sqlalchemy.orm import Relationship
from sqlalchemy.orm import Mapped

from app.config import Base
from app.models.waktu_bimbingan import WaktuBimbingan

from datetime import datetime

class Dosen(Base):
    __tablename__ = "dosen"

    nomor_induk = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    status_kehadiran = Column(String, default=True)
    ketersediaan_bimbingan = Column(Boolean, default=True)
    jumlah_bimbingan = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.now(), nullable=False)
    update_at = Column(DateTime, onupdate=datetime.now(), nullable=False)
    alias = Column(String, nullable=False)

    waktu_bimbingan: Mapped[List[WaktuBimbingan]] = Relationship(back_populates="dosen")
