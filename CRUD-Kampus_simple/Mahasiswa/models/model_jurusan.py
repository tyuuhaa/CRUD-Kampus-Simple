from sqlalchemy import Column, Integer, String
from database.base import Base
from sqlalchemy.orm import relationship

class Jurusan(Base):
    __tablename__ = "jurusan"

    id_jurusan = Column(Integer, primary_key=True, autoincrement=True)
    nama_jurusan = Column(String(100), nullable=False)

    mahasiswa = relationship("Mahasiswa", back_populates="jurusan")  # relasi 1 jurusan -> banyak mahasiswa

    def __repr__(self):
        return f"<Jurusan {self.nama_jurusan}>"
