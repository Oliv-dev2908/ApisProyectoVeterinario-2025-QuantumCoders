from app.crud.base import CRUDBase
from app.models.estudios import Estudio
from app.schemas.estudios import EstudioCreate, EstudioUpdate
from sqlalchemy.orm import Session
from typing import Optional, List

class CRUDEstudio(CRUDBase[Estudio, EstudioCreate, EstudioUpdate]):
    def get(self, db: Session, id: int) -> Optional[Estudio]:
        return db.query(self.model).filter(self.model.id_estudio == id).first()

    def get_multi(self, db: Session, *, skip: int = 0, limit: int = 100):
        return db.query(self.model).offset(skip).limit(limit).all()

    def get_by_paciente(self, db: Session, paciente_id: int) -> List[Estudio]:
        return db.query(self.model).filter(self.model.id_paciente == paciente_id).all()

    def remove(self, db: Session, *, id: int) -> Estudio:
        obj = db.query(self.model).filter(self.model.id_estudio == id).first()
        db.delete(obj)
        db.commit()
        return obj

crud_estudio = CRUDEstudio(Estudio)