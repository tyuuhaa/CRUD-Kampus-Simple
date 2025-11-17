from sqlalchemy import Column, String, Integer, Date, ForeignKey, Table
from database.base import Base
from sqlalchemy.orm import relationship


mahasiswa_matkul = Table(
    "mahasiswa_matkul",
    Base.metadata,
    Column("nim", String(20), ForeignKey("mahasiswa.nim"), primary_key=True),
    Column("id_matkul", Integer, ForeignKey("matakuliah.id_matkul"), primary_key=True)
)
class MataKuliah(Base):
    __tablename__ = "matakuliah"

    id_matkul = Column(Integer, primary_key=True, autoincrement=True)
    nama_matkul = Column(String(100), nullable=False)
    sks = Column(Integer, nullable=False)

    mahasiswa = relationship("Mahasiswa", secondary=mahasiswa_matkul, back_populates="matakuliah")