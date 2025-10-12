from pydantic import BaseModel
from datetime import date
from typing import Optional
from app.schemas.tratamientos import EstadoTratamiento


class FaseTratamientoBase(BaseModel):
    id_tratamiento: int
    descripcion: str
    fecha_programada: date
    fecha_realizada: Optional[date] = None
    costo: float
    estado: EstadoTratamiento

class FaseTratamientoCreate(FaseTratamientoBase):
    pass

class FaseTratamientoUpdate(BaseModel):
    descripcion: Optional[str] = None
    fecha_programada: Optional[date] = None
    fecha_realizada: Optional[date] = None
    costo: Optional[float] = None
    estado: Optional[EstadoTratamiento] = None

class FaseTratamientoResponse(FaseTratamientoBase):
    id_fase: int

    class Config:
        from_attributes = True
