from sqlalchemy import Column, String, Integer, Date, ForeignKey
from sqlalchemy.orm import relationship
from database.base import Base
from .model_jurusan import Jurusan
from .model_matakuliah import MataKuliah, mahasiswa_matkul  # <--- import tabel asosiasi

class Mahasiswa(Base):
    __tablename__ = "mahasiswa"

    nim = Column(String(20), primary_key=True, index=True)
    nama = Column(String(100), nullable=False)
    tahun_masuk = Column(Integer, nullable=False)
    alamat = Column(String)
    tanggal_lahir = Column(Date)
    id_jurusan = Column(Integer, ForeignKey("jurusan.id_jurusan"))

    jurusan = relationship("Jurusan", back_populates="mahasiswa")
    matakuliah = relationship("MataKuliah", secondary=mahasiswa_matkul, back_populates="mahasiswa")
