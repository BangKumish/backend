from typing import List

from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import Relationship
from sqlalchemy.orm import Mapped

from app.config import Base
from app.models.waktu_bimbingan import WaktuBimbingan

from datetime import datetime

class Mahasiswa(Base):
    __tablename__ = "mahasiswa"

    nim = Column(String, primary_key=True)
    nama = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    topik_penelitian = Column(String)
    created_at = Column(DateTime, default=datetime.now(), nullable=False)
    update_at = Column(DateTime, onupdate=datetime.now(), nullable=False)

    waktu_bimbingan: Mapped[List[WaktuBimbingan]] = Relationship(back_populates="mahasiswa")
