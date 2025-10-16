from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Cita(Base):
    __tablename__ = "citas"
    id_cita = Column(Integer, primary_key=True, index=True)
    id_consulta = Column(Integer, ForeignKey("consultas.id_consulta"), nullable=True)  # nuevo campo
    id_paciente = Column(Integer, nullable=False, index=True)
    fecha_hora = Column(DateTime(timezone=True), nullable=False)
    motivo = Column(Text, nullable=True)
    estado = Column(String(100), nullable=True)
    recordatorio_enviado = Column(Boolean, default=False)

    consultas = relationship(
        "Consulta",
        back_populates="cita",
        foreign_keys="[Consulta.id_cita]"  # opcional pero recomendado
    )