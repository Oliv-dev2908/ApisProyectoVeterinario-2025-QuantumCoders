from pydantic import BaseModel
from datetime import date
from typing import Optional

class CirugiaBase(BaseModel):
    id_paciente: int
    id_usuario: int
    fecha: date
    descripcion: str

class CirugiaCreate(CirugiaBase):
    pass

class CirugiaUpdate(BaseModel):
    id_paciente: Optional[int] = None
    id_usuario: Optional[int] = None
    fecha: Optional[date] = None
    descripcion: Optional[str] = None

class CirugiaResponse(CirugiaBase):
    id_cirugia: int

    class Config:
        from_attributes = True