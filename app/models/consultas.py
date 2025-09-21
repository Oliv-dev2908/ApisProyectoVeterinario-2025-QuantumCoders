from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Consulta(Base):
    __tablename__ = "consultas"

    id_consulta = Column(Integer, primary_key=True, index=True)
    id_paciente = Column(Integer, ForeignKey("pacientes.id_paciente"), nullable=False)
    id_usuario = Column(Integer, ForeignKey("usuarios.id_usuario"), nullable=False)
    fecha = Column(DateTime(timezone=True), server_default=func.now())
    motivo = Column(String)
    signosclinicos = Column(String)
    curso = Column(String)
    fechaproxconsulta = Column(DateTime(timezone=True))
    diagnosticopresuntivo = Column(String)
    observaciones = Column(String)

    # Relaciones
    paciente = relationship("Paciente", back_populates="consultas")
    usuario = relationship("Usuario", back_populates="consultas")
    constantes = relationship("ConstanteFisiologica", back_populates="consulta", uselist=False)
    estudios = relationship("Estudio", back_populates="consulta")

class ConstanteFisiologica(Base):
    __tablename__ = "constantes_fisiologicas"

    id_consulta = Column(Integer, ForeignKey("consultas.id_consulta"), primary_key=True)
    peso = Column(Float)
    temperatura = Column(Float)
    pulso = Column(Integer)
    pa = Column(String)  
    fc = Column(Integer)  
    fr = Column(Integer) 
    trc = Column(String) 
    deshidratacion = Column(Float)
    observaciones = Column(String)

    # Relaciones
    consulta = relationship("Consulta", back_populates="constantes")