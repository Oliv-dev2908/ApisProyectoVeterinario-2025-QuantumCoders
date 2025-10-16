from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Consulta(Base):
    __tablename__ = "consultas"

    id_consulta = Column(Integer, primary_key=True, index=True)
    id_paciente = Column(Integer, ForeignKey("pacientes.id_paciente"), nullable=False)
    id_usuario = Column(Integer, ForeignKey("usuarios.id_usuario"), nullable=False)
    fecha = Column(DateTime(timezone=True), server_default=func.now())
    id_cita = Column(Integer, ForeignKey("citas.id_cita"), nullable=True)  # nuevo campo
    motivo = Column(String)
    observaciones = Column(Text, nullable=True)
    signosclinicos = Column(String)
    curso = Column(String)
    fechaproxconsulta = Column(DateTime(timezone=True))
    diagnosticopresuntivo = Column(String)
    condicion = Column(String(100), nullable=True)

    # Relaciones
    paciente = relationship("Paciente", back_populates="consultas")
    usuario = relationship("Usuario", back_populates="consultas")
    cita = relationship("Cita", back_populates="consultas", uselist=False, foreign_keys=[id_cita])  # relación opcional
    constantes = relationship("ConstanteFisiologica", back_populates="consulta",cascade="all, delete", uselist=False)
    estudios = relationship("Estudio", back_populates="consulta")


