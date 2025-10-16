from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class NoAsistenciaBase(BaseModel):
    id_paciente: int
    id_cita: int
    razon: Optional[str] = None

class NoAsistenciaCreate(NoAsistenciaBase):
    pass

class NoAsistenciaUpdate(BaseModel):
    razon: Optional[str] = None

class NoAsistenciaOut(NoAsistenciaBase):
    id_no_asistencia: int
    class Config:
        orm_mode = True