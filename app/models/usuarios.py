from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid
from sqlalchemy.orm import relationship

from app.database import Base

class Usuario(Base):
    __tablename__ = "usuarios"

    id_usuario = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True, index=True)
    rol_id = Column(Integer, nullable=False)
    activo = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), onupdate=func.now())
    supabase_user_id = Column(UUID(as_uuid=True), default=uuid.uuid4)
    consultas = relationship("Consulta", back_populates="usuario")
    cirugias = relationship("Cirugia", back_populates="usuario")
    fisioterapias = relationship("Fisioterapia", back_populates="usuario")
    tratamientos = relationship("Tratamiento", back_populates="usuario")