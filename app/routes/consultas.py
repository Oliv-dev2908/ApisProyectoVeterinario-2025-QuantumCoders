from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.crud.consultas import crud_consulta
from app.schemas.consultas import ConsultaCreate, ConsultaUpdate, ConsultaResponse
# from app.dependencies import get_current_active_user

router = APIRouter()

@router.post("/", response_model=ConsultaResponse, status_code=status.HTTP_201_CREATED)
def create_consulta(
    *,
    db: Session = Depends(get_db),
    consulta_in: ConsultaCreate,
    # current_user = Depends(get_current_active_user)
):
    consulta = crud_consulta.create(db, obj_in=consulta_in)
    return consulta

@router.get("/", response_model=List[ConsultaResponse])
def read_consultas(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    # current_user = Depends(get_current_active_user)
):
    consultas = crud_consulta.get_multi(db, skip=skip, limit=limit)
    return consultas

@router.get("/{consulta_id}", response_model=ConsultaResponse)
def read_consulta(
    *,
    db: Session = Depends(get_db),
    consulta_id: int,
    # current_user = Depends(get_current_active_user)
):
    consulta = crud_consulta.get(db, id=consulta_id)
    if not consulta:
        raise HTTPException(status_code=404, detail="Consulta not found")
    return consulta

@router.get("/paciente/{paciente_id}", response_model=List[ConsultaResponse])
def read_consultas_by_paciente(
    *,
    db: Session = Depends(get_db),
    paciente_id: int,
    # current_user = Depends(get_current_active_user)
):
    consultas = crud_consulta.get_by_paciente(db, paciente_id=paciente_id)
    return consultas

@router.put("/{consulta_id}", response_model=ConsultaResponse)
def update_consulta(
    *,
    db: Session = Depends(get_db),
    consulta_id: int,
    consulta_in: ConsultaUpdate,
    # current_user = Depends(get_current_active_user)
):
    consulta = crud_consulta.get(db, id=consulta_id)
    if not consulta:
        raise HTTPException(status_code=404, detail="Consulta not found")
    consulta = crud_consulta.update(db, db_obj=consulta, obj_in=consulta_in)
    return consulta

@router.delete("/{consulta_id}", response_model=ConsultaResponse)
def delete_consulta(
    *,
    db: Session = Depends(get_db),
    consulta_id: int,
    # current_user = Depends(get_current_active_user)
):
    consulta = crud_consulta.get(db, id=consulta_id)
    if not consulta:
        raise HTTPException(status_code=404, detail="Consulta not found")
    consulta = crud_consulta.remove(db, id=consulta_id)
    return consulta
