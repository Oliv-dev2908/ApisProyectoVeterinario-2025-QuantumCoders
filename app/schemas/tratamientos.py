from pydantic import BaseModel
from datetime import date
from typing import Optional

class TratamientoBase(BaseModel):
    id_paciente: int
    id_usuario: int
    descripcion: str
    fecha_inicio: date
    fecha_fin: date

class TratamientoCreate(TratamientoBase):
    pass

class TratamientoUpdate(BaseModel):
    id_paciente: Optional[int] = None
    id_usuario: Optional[int] = None
    descripcion: Optional[str] = None
    fecha_inicio: Optional[date] = None
    fecha_fin: Optional[date] = None

class TratamientoResponse(TratamientoBase):
    id_tratamiento: int

    class Config:
        from_attributes = True