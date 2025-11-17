from pydantic import BaseModel

class JurusanBase(BaseModel):
    nama_jurusan: str

class JurusanCreate(JurusanBase):
    pass

class JurusanOut(JurusanBase):
    id_jurusan: int

    model_config = {
        "from_attributes": True  # Penting untuk ORM
    }
