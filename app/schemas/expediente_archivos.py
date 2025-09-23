from pydantic import BaseModel
from datetime import datetime
from uuid import UUID
from typing import Optional

class ExpedienteArchivoBase(BaseModel):
    paciente_id: int
    nombre_archivo: str
    url_publica: str
    tipo_archivo: Optional[str] = None

class ExpedienteArchivoCreate(ExpedienteArchivoBase):
    pass

class ExpedienteArchivo(ExpedienteArchivoBase):
    id: UUID
    fecha_subida: datetime

    class Config:
        orm_mode = True
