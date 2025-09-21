from pydantic import BaseModel
from typing import Optional

class ClienteBase(BaseModel):
    nombres: str
    apellidos: str
    telefono: Optional[str] = None
    zona: Optional[str] = None
    calle: Optional[str] = None
    numero: Optional[str] = None

class ClienteCreate(ClienteBase):
    pass

class ClienteUpdate(BaseModel):
    nombres: Optional[str] = None
    apellidos: Optional[str] = None
    telefono: Optional[str] = None
    zona: Optional[str] = None
    calle: Optional[str] = None
    numero: Optional[str] = None

class ClienteResponse(ClienteBase):
    id_cliente: int

    class Config:
        from_attributes = True