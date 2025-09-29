from sqlalchemy import Column, Integer, String, ForeignKey, Date, Text
from sqlalchemy.orm import relationship
from app.database import Base

class Fisioterapia(Base):
    __tablename__ = "fisioterapia"

    id_fisioterapia = Column(Integer, primary_key=True, index=True)
    id_paciente = Column(Integer, ForeignKey("pacientes.id_paciente"), nullable=False)
    id_usuario = Column(Integer, ForeignKey("usuarios.id_usuario"), nullable=False)
    fecha = Column(Date, nullable=False)
    procedimiento = Column(Text, nullable=False)

    # Relaciones
    paciente = relationship("Paciente", back_populates="fisioterapias")
    usuario = relationship("Usuario", back_populates="fisioterapias")