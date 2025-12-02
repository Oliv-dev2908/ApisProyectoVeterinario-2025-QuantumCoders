from app.crud.base import CRUDBase
from app.models.pacientes import Paciente
from app.schemas.pacientes import PacienteCreate, PacienteUpdate
from sqlalchemy.orm import Session
from typing import Optional, List
from sqlalchemy.orm import Session, joinedload
from app.models.pacientes import Paciente
from app.models.clientes import Cliente

class CRUDPaciente(CRUDBase[Paciente, PacienteCreate, PacienteUpdate]):
    def get(self, db: Session, id: int) -> Optional[Paciente]:
        return db.query(self.model).filter(self.model.id_paciente == id).first()

    def get_multi(self, db: Session, *, skip: int = 0, limit: int = 500):
        return db.query(self.model).offset(skip).limit(limit).all()
    
    def get_multi_pas(
        self,
        db: Session,
        *,
        skip: int = 0,
        limit: int = 20,
        search: Optional[str] = None
    ):
        query = (
            db.query(Paciente)
            .join(Cliente)
            .options(joinedload(Paciente.cliente))
        )

        if search:
            query = query.filter(
                Paciente.nombre.ilike(f"%{search}%")
            )

        total = query.count()

        pacientes = (
            query
            .offset(skip)
            .limit(limit)
            .all()
        )

        return pacientes, total

    def get_by_cliente(self, db: Session, cliente_id: int) -> List[Paciente]:
        return db.query(self.model).filter(self.model.id_cliente == cliente_id).all()

    def remove(self, db: Session, *, id: int) -> Paciente:
        obj = db.query(self.model).filter(self.model.id_paciente == id).first()
        db.delete(obj)
        db.commit()
        return obj

crud_paciente = CRUDPaciente(Paciente)
