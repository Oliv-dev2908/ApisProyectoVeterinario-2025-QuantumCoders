from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.crud.fisioterapia import crud_fisioterapia
from app.schemas.fisioterapia import FisioterapiaCreate, FisioterapiaUpdate, FisioterapiaResponse
# from app.dependencies import get_current_active_user

router = APIRouter()

@router.post("/", response_model=FisioterapiaResponse, status_code=status.HTTP_201_CREATED)
def create_fisioterapia(
    *,
    db: Session = Depends(get_db),
    fisioterapia_in: FisioterapiaCreate,
    # current_user = Depends(get_current_active_user)
):
    fisioterapia = crud_fisioterapia.create(db, obj_in=fisioterapia_in)
    return fisioterapia

@router.get("/", response_model=List[FisioterapiaResponse])
def read_fisioterapias(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    # current_user = Depends(get_current_active_user)
):
    fisioterapias = crud_fisioterapia.get_multi(db, skip=skip, limit=limit)
    return fisioterapias

@router.get("/{fisioterapia_id}", response_model=FisioterapiaResponse)
def read_fisioterapia(
    *,
    db: Session = Depends(get_db),
    fisioterapia_id: int,
    # current_user = Depends(get_current_active_user)
):
    fisioterapia = crud_fisioterapia.get(db, id=fisioterapia_id)
    if not fisioterapia:
        raise HTTPException(status_code=404, detail="Fisioterapia not found")
    return fisioterapia

@router.get("/paciente/{paciente_id}", response_model=List[FisioterapiaResponse])
def read_fisioterapias_by_paciente(
    *,
    db: Session = Depends(get_db),
    paciente_id: int,
    # current_user = Depends(get_current_active_user)
):
    fisioterapias = crud_fisioterapia.get_by_paciente(db, paciente_id=paciente_id)
    return fisioterapias

@router.get("/usuario/{usuario_id}", response_model=List[FisioterapiaResponse])
def read_fisioterapias_by_usuario(
    *,
    db: Session = Depends(get_db),
    usuario_id: int,
    # current_user = Depends(get_current_active_user)
):
    fisioterapias = crud_fisioterapia.get_by_usuario(db, usuario_id=usuario_id)
    return fisioterapias

@router.put("/{fisioterapia_id}", response_model=FisioterapiaResponse)
def update_fisioterapia(
    *,
    db: Session = Depends(get_db),
    fisioterapia_id: int,
    fisioterapia_in: FisioterapiaUpdate,
    # current_user = Depends(get_current_active_user)
):
    fisioterapia = crud_fisioterapia.get(db, id=fisioterapia_id)
    if not fisioterapia:
        raise HTTPException(status_code=404, detail="Fisioterapia not found")
    fisioterapia = crud_fisioterapia.update(db, db_obj=fisioterapia, obj_in=fisioterapia_in)
    return fisioterapia

@router.delete("/{fisioterapia_id}", response_model=FisioterapiaResponse)
def delete_fisioterapia(
    *,
    db: Session = Depends(get_db),
    fisioterapia_id: int,
    # current_user = Depends(get_current_active_user)
):
    fisioterapia = crud_fisioterapia.get(db, id=fisioterapia_id)
    if not fisioterapia:
        raise HTTPException(status_code=404, detail="Fisioterapia not found")
    fisioterapia = crud_fisioterapia.remove(db, id=fisioterapia_id)
    return fisioterapia