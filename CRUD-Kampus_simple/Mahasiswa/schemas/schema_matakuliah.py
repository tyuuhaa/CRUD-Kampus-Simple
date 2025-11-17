from pydantic import BaseModel

class MataKuliahBase(BaseModel):
    nama_matkul: str
    sks: int

class MataKuliahCreate(MataKuliahBase):
    pass

class MataKuliahOut(MataKuliahBase):
    id_matkul: int

    model_config = {
        "from_attributes": True
    }
