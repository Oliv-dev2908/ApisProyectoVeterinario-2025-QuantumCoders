from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
import uuid

class UsuarioBase(BaseModel):
    nombre: str
    email: EmailStr
    rol_id: int
    activo: Optional[bool] = True

class UsuarioCreate(UsuarioBase):
    supabase_user_id: Optional[uuid.UUID] = None

class UsuarioUpdate(BaseModel):
    nombre: Optional[str] = None
    email: Optional[EmailStr] = None
    rol_id: Optional[int] = None
    activo: Optional[bool] = None

class UsuarioResponse(UsuarioBase):
    id_usuario: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    supabase_user_id: Optional[uuid.UUID] = None

    class Config:
        orm_mode = True
