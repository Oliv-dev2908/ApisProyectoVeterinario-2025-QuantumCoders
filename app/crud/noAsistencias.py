from typing import Optional, List
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.noAsistencias import NoAsistencia
from app.schemas.noAsistencias import NoAsistenciaCreate, NoAsistenciaUpdate


class CRUDNoAsistencia(CRUDBase[NoAsistencia, NoAsistenciaCreate, NoAsistenciaUpdate]):
    def get(self, db: Session, id: int) -> Optional[NoAsistencia]:
        return db.query(self.model).filter(self.model.id_no_asistencia == id).first()

    def get_multi(self, db: Session, *, skip: int = 0, limit: int = 100) -> List[NoAsistencia]:
        return db.query(self.model).offset(skip).limit(limit).all()

    def get_by_paciente(self, db: Session, paciente_id: int) -> List[NoAsistencia]:
        return db.query(self.model).filter(self.model.id_paciente == paciente_id).all()

    def get_by_cita(self, db: Session, cita_id: int) -> List[NoAsistencia]:
        return db.query(self.model).filter(self.model.id_cita == cita_id).all()

    def remove(self, db: Session, *, id: int) -> Optional[NoAsistencia]:
        obj = self.get(db, id)
        if not obj:
            return None
        db.delete(obj)
        db.commit()
        return obj


crud_no_asistencia = CRUDNoAsistencia(NoAsistencia)
