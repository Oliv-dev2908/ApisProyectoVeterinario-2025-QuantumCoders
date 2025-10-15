from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import and_

from app.crud.base import CRUDBase
from app.models.recordatorios import Recordatorio
from app.schemas.recordatorios import RecordatorioCreate, RecordatorioUpdate


class CRUDRecordatorio(CRUDBase[Recordatorio, RecordatorioCreate, RecordatorioUpdate]):
    def get(self, db: Session, id: int) -> Optional[Recordatorio]:
        return db.query(self.model).filter(self.model.id_recordatorio == id).first()

    def get_multi(self, db: Session, *, skip: int = 0, limit: int = 100) -> List[Recordatorio]:
        return db.query(self.model).offset(skip).limit(limit).all()

    def get_by_cita(self, db: Session, cita_id: int) -> List[Recordatorio]:
        return db.query(self.model).filter(self.model.id_cita == cita_id).all()

    def get_pendientes(self, db: Session) -> List[Recordatorio]:
        # devuelve recordatorios con enviado == False
        return db.query(self.model).filter(self.model.enviado == False).all()

    def mark_enviado(self, db: Session, recordatorio_id: int) -> Optional[Recordatorio]:
        obj = self.get(db, recordatorio_id)
        if not obj:
            return None
        obj.enviado = True
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj

    def remove(self, db: Session, *, id: int) -> Optional[Recordatorio]:
        obj = self.get(db, id)
        if not obj:
            return None
        db.delete(obj)
        db.commit()
        return obj


crud_recordatorio = CRUDRecordatorio(Recordatorio)
