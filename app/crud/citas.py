from typing import Optional, List
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.citas import Cita
from app.schemas.citas import CitaCreate, CitaUpdate


class CRUDCita(CRUDBase[Cita, CitaCreate, CitaUpdate]):
    def get(self, db: Session, id: int) -> Optional[Cita]:
        return db.query(self.model).filter(self.model.id_cita == id).first()

    def get_multi(self, db: Session, *, skip: int = 0, limit: int = 100) -> List[Cita]:
        return db.query(self.model).offset(skip).limit(limit).all()

    def get_by_paciente(self, db: Session, paciente_id: int) -> List[Cita]:
        return db.query(self.model).filter(self.model.id_paciente == paciente_id).all()

    def get_by_estado(self, db: Session, estado: str) -> List[Cita]:
        return db.query(self.model).filter(self.model.estado == estado).all()

    def mark_recordatorio_sent(self, db: Session, cita_id: int) -> Optional[Cita]:
        obj = self.get(db, cita_id)
        if not obj:
            return None
        obj.recordatorio_enviado = True
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj

    def remove(self, db: Session, *, id: int) -> Optional[Cita]:
        obj = self.get(db, id)
        if not obj:
            return None
        db.delete(obj)
        db.commit()
        return obj


crud_cita = CRUDCita(Cita)
