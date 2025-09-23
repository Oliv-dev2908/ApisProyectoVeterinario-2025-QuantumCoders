from sqlalchemy import Column, String, Integer, ForeignKey, Text, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid

from app.database import Base

class ExpedienteArchivo(Base):
    __tablename__ = "expediente_archivos"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    paciente_id = Column(Integer, ForeignKey("pacientes.id_paciente", ondelete="CASCADE"))
    nombre_archivo = Column(Text, nullable=False)
    url_publica = Column(Text, nullable=False)
    tipo_archivo = Column(Text)
    fecha_subida = Column(TIMESTAMP(timezone=True), server_default=func.now())
