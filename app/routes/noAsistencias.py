from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.crud.noAsistencias import crud_no_asistencia
from app.schemas.noAsistencias import NoAsistenciaCreate, NoAsistenciaUpdate, NoAsistenciaOut

router = APIRouter()

# 🟢 Crear una nueva no asistencia
@router.post("/", response_model=NoAsistenciaOut, status_code=status.HTTP_201_CREATED)
def create_no_asistencia(
    *,
    db: Session = Depends(get_db),
    no_asistencia_in: NoAsistenciaCreate
):
    no_asistencia = crud_no_asistencia.create(db, obj_in=no_asistencia_in)
    return no_asistencia


# 🔵 Obtener todas las no asistencias
@router.get("/", response_model=List[NoAsistenciaOut])
def read_no_asistencias(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100
):
    no_asistencias = crud_no_asistencia.get_multi(db, skip=skip, limit=limit)
    return no_asistencias


# 🔵 Obtener una no asistencia por ID
@router.get("/{no_asistencia_id}", response_model=NoAsistenciaOut)
def read_no_asistencia(
    *,
    db: Session = Depends(get_db),
    no_asistencia_id: int
):
    no_asistencia = crud_no_asistencia.get(db, id=no_asistencia_id)
    if not no_asistencia:
        raise HTTPException(status_code=404, detail="No asistencia no encontrada")
    return no_asistencia


# 🔵 Obtener no asistencias por paciente
@router.get("/paciente/{paciente_id}", response_model=List[NoAsistenciaOut])
def read_no_asistencias_by_paciente(
    *,
    db: Session = Depends(get_db),
    paciente_id: int
):
    no_asistencias = crud_no_asistencia.get_by_paciente(db, paciente_id=paciente_id)
    return no_asistencias


# 🔵 Obtener no asistencias por cita
@router.get("/cita/{cita_id}", response_model=List[NoAsistenciaOut])
def read_no_asistencias_by_cita(
    *,
    db: Session = Depends(get_db),
    cita_id: int
):
    no_asistencias = crud_no_asistencia.get_by_cita(db, cita_id=cita_id)
    return no_asistencias


# 🟡 Actualizar una no asistencia
@router.put("/{no_asistencia_id}", response_model=NoAsistenciaOut)
def update_no_asistencia(
    *,
    db: Session = Depends(get_db),
    no_asistencia_id: int,
    no_asistencia_in: NoAsistenciaUpdate
):
    no_asistencia = crud_no_asistencia.get(db, id=no_asistencia_id)
    if not no_asistencia:
        raise HTTPException(status_code=404, detail="No asistencia no encontrada")
    no_asistencia = crud_no_asistencia.update(db, db_obj=no_asistencia, obj_in=no_asistencia_in)
    return no_asistencia


# 🔴 Eliminar una no asistencia
@router.delete("/{no_asistencia_id}", response_model=NoAsistenciaOut)
def delete_no_asistencia(
    *,
    db: Session = Depends(get_db),
    no_asistencia_id: int
):
    no_asistencia = crud_no_asistencia.get(db, id=no_asistencia_id)
    if not no_asistencia:
        raise HTTPException(status_code=404, detail="No asistencia no encontrada")
    no_asistencia = crud_no_asistencia.remove(db, id=no_asistencia_id)
    return no_asistencia
