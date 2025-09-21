from app.crud.base import CRUDBase
from app.models.pacientes import Paciente
from app.schemas.pacientes import PacienteCreate, PacienteUpdate
from sqlalchemy.orm import Session
from typing import Optional, List

class CRUDPaciente(CRUDBase[Paciente, PacienteCreate, PacienteUpdate]):
    def get(self, db: Session, id: int) -> Optional[Paciente]:
        return db.query(self.model).filter(self.model.id_paciente == id).first()

    def get_multi(self, db: Session, *, skip: int = 0, limit: int = 100):
        return db.query(self.model).offset(skip).limit(limit).all()

    def get_by_cliente(self, db: Session, cliente_id: int) -> List[Paciente]:
        return db.query(self.model).filter(self.model.id_cliente == cliente_id).all()

    def remove(self, db: Session, *, id: int) -> Paciente:
        obj = db.query(self.model).filter(self.model.id_paciente == id).first()
        db.delete(obj)
        db.commit()
        return obj

crud_paciente = CRUDPaciente(Paciente)