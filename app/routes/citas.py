from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.crud.citas import crud_cita
from app.schemas.citas import CitaCreate, CitaUpdate, CitaOut

router = APIRouter()

# 🟢 Crear una nueva cita
@router.post("/", response_model=CitaOut, status_code=status.HTTP_201_CREATED)
def create_cita(
    *,
    db: Session = Depends(get_db),
    cita_in: CitaCreate
):
    cita = crud_cita.create(db, obj_in=cita_in)
    return cita


# 🔵 Obtener todas las citas
@router.get("/", response_model=List[CitaOut])
def read_citas(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100
):
    citas = crud_cita.get_multi(db, skip=skip, limit=limit)
    return citas


# 🔵 Obtener una cita por ID
@router.get("/{cita_id}", response_model=CitaOut)
def read_cita(
    *,
    db: Session = Depends(get_db),
    cita_id: int
):
    cita = crud_cita.get(db, id=cita_id)
    if not cita:
        raise HTTPException(status_code=404, detail="Cita no encontrada")
    return cita


# 🔵 Obtener citas por paciente
@router.get("/paciente/{paciente_id}", response_model=List[CitaOut])
def read_citas_by_paciente(
    *,
    db: Session = Depends(get_db),
    paciente_id: int
):
    citas = crud_cita.get_by_paciente(db, paciente_id=paciente_id)
    return citas


# 🔵 Obtener citas por estado
@router.get("/estado/{estado}", response_model=List[CitaOut])
def read_citas_by_estado(
    *,
    db: Session = Depends(get_db),
    estado: str
):
    citas = crud_cita.get_by_estado(db, estado=estado)
    return citas


# 🟡 Actualizar una cita
@router.put("/{cita_id}", response_model=CitaOut)
def update_cita(
    *,
    db: Session = Depends(get_db),
    cita_id: int,
    cita_in: CitaUpdate
):
    cita = crud_cita.get(db, id=cita_id)
    if not cita:
        raise HTTPException(status_code=404, detail="Cita no encontrada")
    cita = crud_cita.update(db, db_obj=cita, obj_in=cita_in)
    return cita


# 🟢 Marcar recordatorio como enviado
@router.put("/{cita_id}/recordatorio", response_model=CitaOut)
def mark_recordatorio_sent(
    *,
    db: Session = Depends(get_db),
    cita_id: int
):
    cita = crud_cita.mark_recordatorio_sent(db, cita_id=cita_id)
    if not cita:
        raise HTTPException(status_code=404, detail="Cita no encontrada")
    return cita


# 🔴 Eliminar una cita
@router.delete("/{cita_id}", response_model=CitaOut)
def delete_cita(
    *,
    db: Session = Depends(get_db),
    cita_id: int
):
    cita = crud_cita.get(db, id=cita_id)
    if not cita:
        raise HTTPException(status_code=404, detail="Cita no encontrada")
    cita = crud_cita.remove(db, id=cita_id)
    return cita
