from app.crud.base import CRUDBase
from app.models.clientes import Cliente
from app.schemas.clientes import ClienteCreate, ClienteUpdate
from sqlalchemy.orm import Session
from typing import Optional

class CRUDCliente(CRUDBase[Cliente, ClienteCreate, ClienteUpdate]):
    def get(self, db: Session, id: int) -> Optional[Cliente]:
        return db.query(self.model).filter(self.model.id_cliente == id).first()

    def get_multi(self, db: Session, *, skip: int = 0, limit: int = 100):
        return db.query(self.model).offset(skip).limit(limit).all()

    def remove(self, db: Session, *, id: int) -> Cliente:
        obj = db.query(self.model).filter(self.model.id_cliente == id).first()
        db.delete(obj)
        db.commit()
        return obj

crud_cliente = CRUDCliente(Cliente)