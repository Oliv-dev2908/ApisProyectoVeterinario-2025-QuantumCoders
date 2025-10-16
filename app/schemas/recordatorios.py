from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class RecordatorioBase(BaseModel):
    id_cita: int
    fecha_envio: datetime
    medio: Optional[str] = None
    enviado: Optional[bool] = False

class RecordatorioCreate(RecordatorioBase):
    pass

class RecordatorioUpdate(BaseModel):
    fecha_envio: Optional[datetime] = None
    medio: Optional[str] = None
    enviado: Optional[bool] = None

class RecordatorioOut(RecordatorioBase):
    id_recordatorio: int
    class Config:
        orm_mode = True