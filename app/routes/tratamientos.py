from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.crud.tratamientos import crud_tratamiento
from app.schemas.tratamientos import TratamientoCreate, TratamientoUpdate, TratamientoResponse
# from app.dependencies import get_current_active_user

router = APIRouter()

@router.post("/", response_model=TratamientoResponse, status_code=status.HTTP_201_CREATED)
def create_tratamiento(
    *,
    db: Session = Depends(get_db),
    tratamiento_in: TratamientoCreate,
    # current_user = Depends(get_current_active_user)
):
    tratamiento = crud_tratamiento.create(db, obj_in=tratamiento_in)
    return tratamiento

@router.get("/", response_model=List[TratamientoResponse])
def read_tratamientos(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    # current_user = Depends(get_current_active_user)
):
    tratamientos = crud_tratamiento.get_multi(db, skip=skip, limit=limit)
    return tratamientos

@router.get("/{tratamiento_id}", response_model=TratamientoResponse)
def read_tratamiento(
    *,
    db: Session = Depends(get_db),
    tratamiento_id: int,
    # current_user = Depends(get_current_active_user)
):
    tratamiento = crud_tratamiento.get(db, id=tratamiento_id)
    if not tratamiento:
        raise HTTPException(status_code=404, detail="Tratamiento not found")
    return tratamiento

@router.get("/paciente/{paciente_id}", response_model=List[TratamientoResponse])
def read_tratamientos_by_paciente(
    *,
    db: Session = Depends(get_db),
    paciente_id: int,
    # current_user = Depends(get_current_active_user)
):
    tratamientos = crud_tratamiento.get_by_paciente(db, paciente_id=paciente_id)
    return tratamientos

@router.get("/usuario/{usuario_id}", response_model=List[TratamientoResponse])
def read_tratamientos_by_usuario(
    *,
    db: Session = Depends(get_db),
    usuario_id: int,
    # current_user = Depends(get_current_active_user)
):
    tratamientos = crud_tratamiento.get_by_usuario(db, usuario_id=usuario_id)
    return tratamientos

@router.put("/{tratamiento_id}", response_model=TratamientoResponse)
def update_tratamiento(
    *,
    db: Session = Depends(get_db),
    tratamiento_id: int,
    tratamiento_in: TratamientoUpdate,
    # current_user = Depends(get_current_active_user)
):
    tratamiento = crud_tratamiento.get(db, id=tratamiento_id)
    if not tratamiento:
        raise HTTPException(status_code=404, detail="Tratamiento not found")
    tratamiento = crud_tratamiento.update(db, db_obj=tratamiento, obj_in=tratamiento_in)
    return tratamiento

@router.delete("/{tratamiento_id}", response_model=TratamientoResponse)
def delete_tratamiento(
    *,
    db: Session = Depends(get_db),
    tratamiento_id: int,
    # current_user = Depends(get_current_active_user)
):
    tratamiento = crud_tratamiento.get(db, id=tratamiento_id)
    if not tratamiento:
        raise HTTPException(status_code=404, detail="Tratamiento not found")
    tratamiento = crud_tratamiento.remove(db, id=tratamiento_id)
    return tratamiento