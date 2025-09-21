from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class EstudioBase(BaseModel):
    id_paciente: int
    id_consulta: Optional[int] = None
    tipo_estudio: str
    resultado: Optional[str] = None
    archivo_url: Optional[str] = None

class EstudioCreate(EstudioBase):
    pass

class EstudioUpdate(BaseModel):
    id_paciente: Optional[int] = None
    id_consulta: Optional[int] = None
    tipo_estudio: Optional[str] = None
    resultado: Optional[str] = None
    archivo_url: Optional[str] = None

class EstudioResponse(EstudioBase):
    id_estudio: int
    fecha: datetime

    class Config:
        from_attributes = True