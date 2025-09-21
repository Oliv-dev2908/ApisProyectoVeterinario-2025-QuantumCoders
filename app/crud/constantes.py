from app.crud.base import CRUDBase
from app.models.consultas import ConstanteFisiologica
from app.schemas.constantes import ConstanteCreate, ConstanteUpdate
from sqlalchemy.orm import Session
from typing import Optional

class CRUDConstante(CRUDBase[ConstanteFisiologica, ConstanteCreate, ConstanteUpdate]):
    def get(self, db: Session, id: int) -> Optional[ConstanteFisiologica]:
        return db.query(self.model).filter(self.model.id_consulta == id).first()

    def get_multi(self, db: Session, *, skip: int = 0, limit: int = 100):
        return db.query(self.model).offset(skip).limit(limit).all()

    def remove(self, db: Session, *, id: int) -> ConstanteFisiologica:
        obj = db.query(self.model).filter(self.model.id_consulta == id).first()
        db.delete(obj)
        db.commit()
        return obj

crud_constante = CRUDConstante(ConstanteFisiologica)