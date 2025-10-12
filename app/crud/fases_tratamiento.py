from app.crud.base import CRUDBase
from app.models.fases_tratamiento import FaseTratamiento
from app.models.tratamientos import Tratamiento
from app.schemas.fases_tratamiento import FaseTratamientoCreate, FaseTratamientoUpdate
from sqlalchemy.orm import Session
from typing import List, Optional

class CRUDFaseTratamiento(CRUDBase[FaseTratamiento, FaseTratamientoCreate, FaseTratamientoUpdate]):
    def get_by_tratamiento(self, db: Session, tratamiento_id: int) -> List[FaseTratamiento]:
        return db.query(self.model).filter(self.model.id_tratamiento == tratamiento_id).all()
    def get_by_id_fase(self, db: Session, id_fase: int) -> Optional[FaseTratamiento]:
        return db.query(self.model).filter(self.model.id_fase == id_fase).first()
    def add_price_tratamiento(self, price: float, db: Session, tratamiento_id: int):
        tratamiento = db.query(Tratamiento).filter(Tratamiento.id_tratamiento == tratamiento_id).first()
        if tratamiento:
            tratamiento.costo += price
            db.commit()
            db.refresh(tratamiento)
    

crud_fase_tratamiento = CRUDFaseTratamiento(FaseTratamiento)
