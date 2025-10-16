from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Recordatorio(Base):
    __tablename__ = "recordatorios"
    id_recordatorio = Column(Integer, primary_key=True, index=True)
    id_cita = Column(Integer, nullable=False, index=True)
    fecha_envio = Column(DateTime(timezone=True), nullable=False)
    medio = Column(String(100), nullable=True)
    enviado = Column(Boolean, default=False)