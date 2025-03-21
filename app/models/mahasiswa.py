from typing import List

from sqlalchemy import Column, String
from sqlalchemy.orm import Relationship
from sqlalchemy.orm import Mapped

from app.config import Base
from app.models.waktu_bimbingan import WaktuBimbingan

class Mahasiswa(Base):
    __tablename__ = "mahasiswa"

    nim = Column(String, primary_key=True)
    nama = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    topik_penelitian = Column(String)

    waktu_bimbingan: Mapped[List[WaktuBimbingan]] = Relationship(back_populates="mahasiswa")
