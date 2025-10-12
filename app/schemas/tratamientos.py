from pydantic import BaseModel
from datetime import date
from typing import Optional
from enum import Enum

class EstadoTratamiento(str, Enum):
    pendiente = "pendiente"
    completada = "completada"
    cancelada = "cancelada"

class TratamientoBase(BaseModel):
    id_paciente: int
    id_usuario: int
    tipo: str
    descripcion: str
    fecha_inicio: date
    costo: float
    estado: EstadoTratamiento
    gravedad: str

class TratamientoCreate(TratamientoBase):
    pass

class TratamientoUpdate(BaseModel):
    id_paciente: Optional[int] = None
    id_usuario: Optional[int] = None
    tipo: Optional[str] = None
    descripcion: Optional[str] = None
    fecha_inicio: Optional[date] = None
    costo: Optional[float] = None
    estado: Optional[EstadoTratamiento] = None
    gravedad: Optional[str] = None

class TratamientoResponse(TratamientoBase):
    id_tratamiento: int

    class Config:
        from_attributes = True