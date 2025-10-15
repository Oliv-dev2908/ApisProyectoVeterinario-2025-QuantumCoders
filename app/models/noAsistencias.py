from sqlalchemy import Column, Integer, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class NoAsistencia(Base):
    __tablename__ = "no_asistencias"
    id_no_asistencia = Column(Integer, primary_key=True, index=True)
    id_paciente = Column(Integer, nullable=False, index=True)
    id_cita = Column(Integer, nullable=False, index=True)
    razon = Column(Text, nullable=True)