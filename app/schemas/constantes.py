from pydantic import BaseModel
from typing import Optional

class ConstanteBase(BaseModel):
    peso: Optional[float] = None
    temperatura: Optional[float] = None
    pulso: Optional[int] = None
    pa: Optional[str] = None
    fc: Optional[int] = None
    fr: Optional[int] = None
    trc: Optional[str] = None
    deshidratacion: Optional[float] = None
    observaciones: Optional[str] = None

class ConstanteCreate(ConstanteBase):
    id_consulta: int

class ConstanteUpdate(ConstanteBase):
    pass

class ConstanteResponse(ConstanteBase):
    id_consulta: int

    class Config:
        from_attributes = True