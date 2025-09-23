from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.schemas.expediente_archivos import ExpedienteArchivo, ExpedienteArchivoCreate
from app.crud import expediente_archivos as crud

router = APIRouter()

@router.post("/", response_model=ExpedienteArchivo)
def create_expediente_archivo(archivo: ExpedienteArchivoCreate, db: Session = Depends(get_db)):
    return crud.create_archivo(db=db, archivo=archivo)

@router.get("/", response_model=List[ExpedienteArchivo])
def read_expediente_archivos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_archivos(db, skip=skip, limit=limit)

@router.get("/{archivo_id}", response_model=ExpedienteArchivo)
def read_expediente_archivo(archivo_id: str, db: Session = Depends(get_db)):
    db_archivo = crud.get_archivo(db, archivo_id=archivo_id)
    if db_archivo is None:
        raise HTTPException(status_code=404, detail="Archivo no encontrado")
    return db_archivo

@router.delete("/{archivo_id}", response_model=ExpedienteArchivo)
def delete_expediente_archivo(archivo_id: str, db: Session = Depends(get_db)):
    db_archivo = crud.delete_archivo(db, archivo_id=archivo_id)
    if db_archivo is None:
        raise HTTPException(status_code=404, detail="Archivo no encontrado")
    return db_archivo

@router.get("/paciente/{paciente_id}", response_model=list[ExpedienteArchivo])
def get_archivos_paciente(paciente_id: int, db: Session = Depends(get_db)):
    archivos = crud.get_archivos_by_paciente(db, paciente_id)
    if not archivos:
        raise HTTPException(status_code=404, detail="No se encontraron archivos para este paciente")
    return archivos
