from sqlalchemy import Column, Integer, Date, ForeignKey, Float, Enum, Text
from sqlalchemy.orm import relationship
from app.database import Base
from app.models.tratamientos import EstadoTratamiento
import enum


class FaseTratamiento(Base):
    __tablename__ = "fases_tratamiento"

    id_fase = Column(Integer, primary_key=True, index=True)
    id_tratamiento = Column(Integer, ForeignKey("tratamientos.id_tratamiento"), nullable=False)
    descripcion = Column(Text, nullable=False)
    fecha_programada = Column(Date, nullable=False)
    fecha_realizada = Column(Date, nullable=False)
    costo = Column(Float, nullable=False)
    estado = Column(Enum(EstadoTratamiento), nullable=False, default=EstadoTratamiento.pendiente)

    tratamiento = relationship("Tratamiento", back_populates="fases")