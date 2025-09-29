from pydantic import BaseModel
from datetime import date
from typing import Optional

class FisioterapiaBase(BaseModel):
    id_paciente: int
    id_usuario: int
    fecha: date
    procedimiento: str

class FisioterapiaCreate(FisioterapiaBase):
    pass

class FisioterapiaUpdate(BaseModel):
    id_paciente: Optional[int] = None
    id_usuario: Optional[int] = None
    fecha: Optional[date] = None
    procedimiento: Optional[str] = None

class FisioterapiaResponse(FisioterapiaBase):
    id_fisioterapia: int

    class Config:
        from_attributes = True