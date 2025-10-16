from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ConsultaBase(BaseModel):
    id_paciente: int
    id_usuario: int
    id_cita: Optional[int] = None
    motivo: Optional[str] = None
    signosclinicos: Optional[str] = None
    curso: Optional[str] = None
    fechaproxconsulta: Optional[datetime] = None
    diagnosticopresuntivo: Optional[str] = None
    observaciones: Optional[str] = None
    fecha: datetime
    condicion: Optional[str] = None


class ConsultaCreate(ConsultaBase):
    pass

class ConsultaUpdate(BaseModel):
    id_paciente: Optional[int] = None
    id_usuario: Optional[int] = None
    id_cita: Optional[int] = None
    motivo: Optional[str] = None
    signosclinicos: Optional[str] = None
    curso: Optional[str] = None
    fechaproxconsulta: Optional[datetime] = None
    diagnosticopresuntivo: Optional[str] = None
    observaciones: Optional[str] = None
    condicion: Optional[str] = None


class ConsultaResponse(ConsultaBase):
    id_consulta: int
    fecha: datetime

    class Config:
        from_attributes = True