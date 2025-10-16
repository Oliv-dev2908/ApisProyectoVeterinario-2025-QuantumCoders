from app.crud.base import CRUDBase
from app.models.consultas import Consulta
from app.schemas.consultas import ConsultaCreate, ConsultaUpdate
from sqlalchemy.orm import Session
from typing import Optional, List

class CRUDConsulta(CRUDBase[Consulta, ConsultaCreate, ConsultaUpdate]):
    def get(self, db: Session, id: int) -> Optional[Consulta]:
        return db.query(self.model).filter(self.model.id_consulta == id).first()

    def get_multi(self, db: Session, *, skip: int = 0, limit: int = 100):
        return db.query(self.model).offset(skip).limit(limit).all()

    def get_by_paciente(self, db: Session, paciente_id: int) -> List[Consulta]:
        return db.query(self.model).filter(self.model.id_paciente == paciente_id).all()

    def remove(self, db: Session, *, id: int) -> Consulta:
        obj = db.query(self.model).filter(self.model.id_consulta == id).first()
        db.delete(obj)
        db.commit()
        return obj

    def get_by_usuario(self, db: Session, usuario_id: int) -> List[Consulta]:
        return db.query(self.model).filter(self.model.id_usuario == usuario_id).all()

    def get_proximas_por_paciente(self, db: Session, paciente_id: int) -> List[Consulta]:
        # ejemplo: retornar consultas con fechaproxconsulta no nula
        return db.query(self.model).filter(
            self.model.id_paciente == paciente_id,
            self.model.fechaproxconsulta.isnot(None)
        ).all()

crud_consulta = CRUDConsulta(Consulta)