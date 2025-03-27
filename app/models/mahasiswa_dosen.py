from sqlalchemy import Column, String, ForeignKey, Integer, UniqueConstraint, DateTime
from sqlalchemy.orm import relationship, validates
from app.config import Base

from datetime import datetime
class MahasiswaDosen(Base):
    __tablename__ = "mahasiswa_dosen"

    id = Column(Integer, primary_key=True, autoincrement=True)
    mahasiswa_nim = Column(String, ForeignKey("mahasiswa.nim"), nullable=False)
    dosen_id = Column(String, ForeignKey("dosen.nomor_induk"))
    role = Column(String)
    created_at = Column(DateTime, default=datetime.now(), nullable=False)
    update_at = Column(DateTime, onupdate=datetime.now(), nullable=False)

    mahasiswa = relationship("Mahasiswa", back_populates="dosen_relations")
    dosen = relationship("Dosen", back_populates="mahasiswa_relations")

    @validates("mahasiswa_nim")
    def validate_dosen_count(self, key, mahasiswa_nim):
        from sqlalchemy.orm import Session
        from app.config import SessionLocal

        db: Session = SessionLocal()
        count_advisors = db.query(MahasiswaDosen).filter(
            MahasiswaDosen.mahasiswa_nim == mahasiswa_nim,
            MahasiswaDosen.role.like("Dosen Pembimbing%")
        ).count()
        count_examiners = db.query(MahasiswaDosen).filter(
            MahasiswaDosen.mahasiswa_nim == mahasiswa_nim,
            MahasiswaDosen.role.like("Dosen Penguji%")
        ).count()

        if "Dosen Pembimbing" in self.role and count_advisors >= 2:
            raise ValueError("Maksimal 2 Dosen Pembimbing")
        if "Dosen Penguji" in self.role and count_examiners >= 2:
            raise ValueError("Maksimal 2 Dosen Penguji")
        
        return mahasiswa_nim
    
    __table_args__ = (
        UniqueConstraint("mahasiswa_nim", "dosen_id", "role", name="unique_mahasiswa_dosen_role"),
    )