from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class UsuarioBase(BaseModel):
    nombre: str
    email: str
    rol_id: int
    activo: bool = True

class UsuarioCreate(UsuarioBase):
    contraseña: str

class UsuarioUpdate(BaseModel):
    nombre: Optional[str] = None
    email: Optional[str] = None
    rol_id: Optional[int] = None
    activo: Optional[bool] = None
    contraseña: Optional[str] = None

class UsuarioResponse(UsuarioBase):
    id_usuario: int
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True

class LoginRequest(BaseModel):
    email: str
    contraseña: str

class Token(BaseModel):
    access_token: str
    token_type: str