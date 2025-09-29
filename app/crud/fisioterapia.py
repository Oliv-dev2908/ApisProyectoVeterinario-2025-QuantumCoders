from app.crud.base import CRUDBase
from app.models.fisioterapia import Fisioterapia
from app.schemas.fisioterapia import FisioterapiaCreate, FisioterapiaUpdate
from sqlalchemy.orm import Session
from typing import Optional, List

class CRUDFisioterapia(CRUDBase[Fisioterapia, FisioterapiaCreate, FisioterapiaUpdate]):
    def get(self, db: Session, id: int) -> Optional[Fisioterapia]:
        return db.query(self.model).filter(self.model.id_fisioterapia == id).first()

    def get_multi(self, db: Session, *, skip: int = 0, limit: int = 100):
        return db.query(self.model).offset(skip).limit(limit).all()

    def get_by_paciente(self, db: Session, paciente_id: int) -> List[Fisioterapia]:
        return db.query(self.model).filter(self.model.id_paciente == paciente_id).all()

    def get_by_usuario(self, db: Session, usuario_id: int) -> List[Fisioterapia]:
        return db.query(self.model).filter(self.model.id_usuario == usuario_id).all()

    def remove(self, db: Session, *, id: int) -> Fisioterapia:
        obj = db.query(self.model).filter(self.model.id_fisioterapia == id).first()
        db.delete(obj)
        db.commit()
        return obj

crud_fisioterapia = CRUDFisioterapia(Fisioterapia)