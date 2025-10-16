from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.crud.recordatorios import crud_recordatorio
from app.schemas.recordatorios import RecordatorioCreate, RecordatorioUpdate, RecordatorioOut

router = APIRouter()

# 🟢 Crear un recordatorio
@router.post("/", response_model=RecordatorioOut, status_code=status.HTTP_201_CREATED)
def create_recordatorio(
    *,
    db: Session = Depends(get_db),
    recordatorio_in: RecordatorioCreate
):
    recordatorio = crud_recordatorio.create(db, obj_in=recordatorio_in)
    return recordatorio


# 🔵 Obtener todos los recordatorios
@router.get("/", response_model=List[RecordatorioOut])
def read_recordatorios(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100
):
    recordatorios = crud_recordatorio.get_multi(db, skip=skip, limit=limit)
    return recordatorios


# 🔵 Obtener un recordatorio por ID
@router.get("/{recordatorio_id}", response_model=RecordatorioOut)
def read_recordatorio(
    *,
    db: Session = Depends(get_db),
    recordatorio_id: int
):
    recordatorio = crud_recordatorio.get(db, id=recordatorio_id)
    if not recordatorio:
        raise HTTPException(status_code=404, detail="Recordatorio no encontrado")
    return recordatorio


# 🔵 Obtener recordatorios por cita
@router.get("/cita/{cita_id}", response_model=List[RecordatorioOut])
def read_recordatorios_by_cita(
    *,
    db: Session = Depends(get_db),
    cita_id: int
):
    recordatorios = crud_recordatorio.get_by_cita(db, cita_id=cita_id)
    return recordatorios


# 🔵 Obtener recordatorios pendientes (no enviados)
@router.get("/pendientes", response_model=List[RecordatorioOut])
def read_recordatorios_pendientes(
    db: Session = Depends(get_db)
):
    recordatorios = crud_recordatorio.get_pendientes(db)
    return recordatorios


# 🟡 Marcar un recordatorio como enviado
@router.put("/enviar/{recordatorio_id}", response_model=RecordatorioOut)
def mark_recordatorio_enviado(
    *,
    db: Session = Depends(get_db),
    recordatorio_id: int
):
    recordatorio = crud_recordatorio.mark_enviado(db, recordatorio_id=recordatorio_id)
    if not recordatorio:
        raise HTTPException(status_code=404, detail="Recordatorio no encontrado")
    return recordatorio


# 🟡 Actualizar un recordatorio
@router.put("/{recordatorio_id}", response_model=RecordatorioOut)
def update_recordatorio(
    *,
    db: Session = Depends(get_db),
    recordatorio_id: int,
    recordatorio_in: RecordatorioUpdate
):
    recordatorio = crud_recordatorio.get(db, id=recordatorio_id)
    if not recordatorio:
        raise HTTPException(status_code=404, detail="Recordatorio no encontrado")
    recordatorio = crud_recordatorio.upda_
