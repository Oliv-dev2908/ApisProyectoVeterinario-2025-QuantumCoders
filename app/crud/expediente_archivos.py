from sqlalchemy.orm import Session
from app.models.expediente_archivos import ExpedienteArchivo
from app.schemas.expediente_archivos import ExpedienteArchivoCreate

def get_archivos(db: Session, skip: int = 0, limit: int = 100):
    return db.query(ExpedienteArchivo).offset(skip).limit(limit).all()

def get_archivo(db: Session, archivo_id: str):
    return db.query(ExpedienteArchivo).filter(ExpedienteArchivo.id == archivo_id).first()

def create_archivo(db: Session, archivo: ExpedienteArchivoCreate):
    db_archivo = ExpedienteArchivo(**archivo.dict())
    db.add(db_archivo)
    db.commit()
    db.refresh(db_archivo)
    return db_archivo

def delete_archivo(db: Session, archivo_id: str):
    db_archivo = db.query(ExpedienteArchivo).filter(ExpedienteArchivo.id == archivo_id).first()
    if db_archivo:
        db.delete(db_archivo)
        db.commit()
    return db_archivo
