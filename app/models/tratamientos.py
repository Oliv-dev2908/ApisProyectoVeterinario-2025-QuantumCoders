from sqlalchemy import Column, Integer, String, ForeignKey, Date, Text, Enum, Float
from sqlalchemy.orm import relationship
from app.database import Base
import enum

class EstadoTratamiento(enum.Enum):
    pendiente = "pendiente"
    completado = "completado"
    cancelada = "cancelada"
class Tratamiento(Base):
    __tablename__ = "tratamientos"

    id_tratamiento = Column(Integer, primary_key=True, index=True)
    id_paciente = Column(Integer, ForeignKey("pacientes.id_paciente"), nullable=False)
    id_usuario = Column(Integer, ForeignKey("usuarios.id_usuario"), nullable=False)
    tipo = Column(String, nullable=False)
    descripcion = Column(Text, nullable=False)
    fecha_inicio = Column(Date, nullable=False)
    costo = Column(Float, nullable=False)
    estado = Column(Enum(EstadoTratamiento), nullable=False, default=EstadoTratamiento.pendiente)
    gravedad = Column(String, nullable=False)
    

    # Relaciones
    paciente = relationship("Paciente", back_populates="tratamientos")
    usuario = relationship("Usuario", back_populates="tratamientos")

    # Relacion con fases
    fases = relationship("FaseTratamiento", back_populates="tratamiento", cascade="all, delete-orphan")