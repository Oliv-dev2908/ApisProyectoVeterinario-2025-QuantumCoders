from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base

class Cliente(Base):
    __tablename__ = "clientes"

    id_cliente = Column(Integer, primary_key=True, index=True)
    nombres = Column(String, nullable=False)
    apellidos = Column(String, nullable=False)
    telefono = Column(String)
    zona = Column(String)
    calle = Column(String)
    numero = Column(String)

    # Tablas relacionadas
    pacientes = relationship("Paciente", back_populates="cliente")
