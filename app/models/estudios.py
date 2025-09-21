from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Estudio(Base):
    __tablename__ = "estudios"

    id_estudio = Column(Integer, primary_key=True, index=True)
    id_paciente = Column(Integer, ForeignKey("pacientes.id_paciente"), nullable=False)
    id_consulta = Column(Integer, ForeignKey("consultas.id_consulta"))
    tipo_estudio = Column(String, nullable=False)
    fecha = Column(DateTime(timezone=True), server_default=func.now())
    resultado = Column(String)
    archivo_url = Column(String)

    # Relaciones
    paciente = relationship("Paciente", back_populates="estudios")
    consulta = relationship("Consulta", back_populates="estudios")