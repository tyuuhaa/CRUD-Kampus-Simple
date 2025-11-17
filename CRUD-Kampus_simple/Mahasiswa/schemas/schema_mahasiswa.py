from pydantic import BaseModel
from typing import List, Optional
from datetime import date
from schemas.schema_jurusan import JurusanOut
from schemas.schema_matakuliah import MataKuliahOut

class MahasiswaBase(BaseModel):
    nim: str
    nama: str
    tahun_masuk: int
    alamat: Optional[str] = None
    tanggal_lahir: Optional[date] = None
    id_jurusan: Optional[int] = None
    matkul_ids: Optional[List[int]] = []

class MahasiswaCreate(MahasiswaBase):
    pass

class MahasiswaOut(MahasiswaBase):
    jurusan: Optional[JurusanOut] = None
    matakuliah: List[MataKuliahOut] = []

    model_config = {
        "from_attributes": True
    }
