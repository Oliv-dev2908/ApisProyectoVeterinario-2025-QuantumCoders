from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

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