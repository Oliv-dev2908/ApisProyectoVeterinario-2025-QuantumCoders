from app.crud.base import CRUDBase
from app.models.cirugias import Cirugia
from app.schemas.cirugias import CirugiaCreate, CirugiaUpdate
from sqlalchemy.orm import Session
from typing import Optional, List

class CRUDCirugia(CRUDBase[Cirugia, CirugiaCreate, CirugiaUpdate]):
    def get(self, db: Session, id: int) -> Optional[Cirugia]:
        return db.query(self.model).filter(self.model.id_cirugia == id).first()

    def get_multi(self, db: Session, *, skip: int = 0, limit: int = 100):
        return db.query(self.model).offset(skip).limit(limit).all()

    def get_by_paciente(self, db: Session, paciente_id: int) -> List[Cirugia]:
        return db.query(self.model).filter(self.model.id_paciente == paciente_id).all()

    def get_by_usuario(self, db: Session, usuario_id: int) -> List[Cirugia]:
        return db.query(self.model).filter(self.model.id_usuario == usuario_id).all()

    def remove(self, db: Session, *, id: int) -> Cirugia:
        obj = db.query(self.model).filter(self.model.id_cirugia == id).first()
        db.delete(obj)
        db.commit()
        return obj

crud_cirugia = CRUDCirugia(Cirugia)