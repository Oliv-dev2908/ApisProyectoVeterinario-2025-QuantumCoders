from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Paciente(Base):
    __tablename__ = "pacientes"

    id_paciente = Column(Integer, primary_key=True, index=True)
    id_cliente = Column(Integer, ForeignKey("clientes.id_cliente"), nullable=False)
    nombre = Column(String, nullable=False)
    especie = Column(String, nullable=False)
    raza = Column(String)
    edad = Column(Integer)
    sexo = Column(String)
    color = Column(String)
    tamanocm = Column(Float)
    estado_reproductivo = Column(String)
    gestacion = Column(String)
    alimentacion = Column(String)
    cirugiasprevias = Column(String)
    estado = Column(String)
    estado_corporal = Column(String)
    peso = Column(Float)
    foto_url = Column(String)
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())

    # Relaciones
    cliente = relationship("Cliente", back_populates="pacientes")
    consultas = relationship("Consulta", back_populates="paciente")
    estudios = relationship("Estudio", back_populates="paciente")