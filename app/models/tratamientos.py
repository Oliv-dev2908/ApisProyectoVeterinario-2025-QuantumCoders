from sqlalchemy import Column, Integer, String, ForeignKey, Date, Text
from sqlalchemy.orm import relationship
from app.database import Base

class Tratamiento(Base):
    __tablename__ = "tratamientos"

    id_tratamiento = Column(Integer, primary_key=True, index=True)
    id_paciente = Column(Integer, ForeignKey("pacientes.id_paciente"), nullable=False)
    id_usuario = Column(Integer, ForeignKey("usuarios.id_usuario"), nullable=False)
    descripcion = Column(Text, nullable=False)
    fecha_inicio = Column(Date, nullable=False)
    fecha_fin = Column(Date, nullable=False)

    # Relaciones
    paciente = relationship("Paciente", back_populates="tratamientos")
    usuario = relationship("Usuario", back_populates="tratamientos")