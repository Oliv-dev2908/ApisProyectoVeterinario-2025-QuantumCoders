from app.crud.base import CRUDBase
from app.models.tratamientos import Tratamiento
from app.schemas.tratamientos import TratamientoCreate, TratamientoUpdate
from sqlalchemy.orm import Session
from typing import Optional, List

class CRUDTratamiento(CRUDBase[Tratamiento, TratamientoCreate, TratamientoUpdate]):
    def get(self, db: Session, id: int) -> Optional[Tratamiento]:
        return db.query(self.model).filter(self.model.id_tratamiento == id).first()

    def get_multi(self, db: Session, *, skip: int = 0, limit: int = 100):
        return db.query(self.model).offset(skip).limit(limit).all()

    def get_by_paciente(self, db: Session, paciente_id: int) -> List[Tratamiento]:
        return db.query(self.model).filter(self.model.id_paciente == paciente_id).all()

    def get_by_usuario(self, db: Session, usuario_id: int) -> List[Tratamiento]:
        return db.query(self.model).filter(self.model.id_usuario == usuario_id).all()

    def remove(self, db: Session, *, id: int) -> Tratamiento:
        obj = db.query(self.model).filter(self.model.id_tratamiento == id).first()
        db.delete(obj)
        db.commit()
        return obj

crud_tratamiento = CRUDTratamiento(Tratamiento)