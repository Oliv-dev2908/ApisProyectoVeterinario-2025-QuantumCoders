from sqlalchemy import Column, Integer, String, ForeignKey, Date, Text
from sqlalchemy.orm import relationship
from app.database import Base

class Cirugia(Base):
    __tablename__ = "cirugias"

    id_cirugia = Column(Integer, primary_key=True, index=True)
    id_paciente = Column(Integer, ForeignKey("pacientes.id_paciente"), nullable=False)
    id_usuario = Column(Integer, ForeignKey("usuarios.id_usuario"), nullable=False)
    fecha = Column(Date, nullable=False)
    descripcion = Column(Text, nullable=False)

    # Relaciones
    paciente = relationship("Paciente", back_populates="cirugias")
    usuario = relationship("Usuario", back_populates="cirugias")