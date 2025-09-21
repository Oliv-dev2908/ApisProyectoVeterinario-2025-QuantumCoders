from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class PacienteBase(BaseModel):
    id_cliente: int
    nombre: str
    especie: str
    raza: Optional[str] = None
    edad: Optional[int] = None
    sexo: Optional[str] = None
    color: Optional[str] = None
    tamanocm: Optional[float] = None
    estado_reproductivo: Optional[str] = None
    gestacion: Optional[str] = None
    alimentacion: Optional[str] = None
    cirugiasprevias: Optional[str] = None
    estado: Optional[str] = None
    estado_corporal: Optional[str] = None
    peso: Optional[float] = None
    foto_url: Optional[str] = None

class PacienteCreate(PacienteBase):
    pass

class PacienteUpdate(BaseModel):
    id_cliente: Optional[int] = None
    nombre: Optional[str] = None
    especie: Optional[str] = None
    raza: Optional[str] = None
    edad: Optional[int] = None
    sexo: Optional[str] = None
    color: Optional[str] = None
    tamanocm: Optional[float] = None
    estado_reproductivo: Optional[str] = None
    gestacion: Optional[str] = None
    alimentacion: Optional[str] = None
    cirugiasprevias: Optional[str] = None
    estado: Optional[str] = None
    estado_corporal: Optional[str] = None
    peso: Optional[float] = None
    foto_url: Optional[str] = None

class PacienteResponse(PacienteBase):
    id_paciente: int
    fecha_creacion: datetime

    class Config:
        from_attributes = True