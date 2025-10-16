from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class CitaBase(BaseModel):
    id_paciente: int
    id_consulta: Optional[int] = None
    fecha_hora: datetime
    motivo: Optional[str] = None
    estado: Optional[str] = None
    recordatorio_enviado: Optional[bool] = False

class CitaCreate(CitaBase):
    pass

class CitaUpdate(BaseModel):
    id_consulta: Optional[int] = None
    fecha_hora: Optional[datetime] = None
    motivo: Optional[str] = None
    estado: Optional[str] = None
    recordatorio_enviado: Optional[bool] = None

class CitaOut(CitaBase):
    id_cita: int
    class Config:
        orm_mode = True