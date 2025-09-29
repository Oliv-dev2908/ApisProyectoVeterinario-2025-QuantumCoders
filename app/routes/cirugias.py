from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.crud.cirugias import crud_cirugia
from app.schemas.cirugias import CirugiaCreate, CirugiaUpdate, CirugiaResponse
# from app.dependencies import get_current_active_user

router = APIRouter()

@router.post("/", response_model=CirugiaResponse, status_code=status.HTTP_201_CREATED)
def create_cirugia(
    *,
    db: Session = Depends(get_db),
    cirugia_in: CirugiaCreate,
    # current_user = Depends(get_current_active_user)
):
    cirugia = crud_cirugia.create(db, obj_in=cirugia_in)
    return cirugia

@router.get("/", response_model=List[CirugiaResponse])
def read_cirugias(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    # current_user = Depends(get_current_active_user)
):
    cirugias = crud_cirugia.get_multi(db, skip=skip, limit=limit)
    return cirugias

@router.get("/{cirugia_id}", response_model=CirugiaResponse)
def read_cirugia(
    *,
    db: Session = Depends(get_db),
    cirugia_id: int,
    # current_user = Depends(get_current_active_user)
):
    cirugia = crud_cirugia.get(db, id=cirugia_id)
    if not cirugia:
        raise HTTPException(status_code=404, detail="Cirugia not found")
    return cirugia

@router.get("/paciente/{paciente_id}", response_model=List[CirugiaResponse])
def read_cirugias_by_paciente(
    *,
    db: Session = Depends(get_db),
    paciente_id: int,
    # current_user = Depends(get_current_active_user)
):
    cirugias = crud_cirugia.get_by_paciente(db, paciente_id=paciente_id)
    return cirugias

@router.get("/usuario/{usuario_id}", response_model=List[CirugiaResponse])
def read_cirugias_by_usuario(
    *,
    db: Session = Depends(get_db),
    usuario_id: int,
    # current_user = Depends(get_current_active_user)
):
    cirugias = crud_cirugia.get_by_usuario(db, usuario_id=usuario_id)
    return cirugias

@router.put("/{cirugia_id}", response_model=CirugiaResponse)
def update_cirugia(
    *,
    db: Session = Depends(get_db),
    cirugia_id: int,
    cirugia_in: CirugiaUpdate,
    # current_user = Depends(get_current_active_user)
):
    cirugia = crud_cirugia.get(db, id=cirugia_id)
    if not cirugia:
        raise HTTPException(status_code=404, detail="Cirugia not found")
    cirugia = crud_cirugia.update(db, db_obj=cirugia, obj_in=cirugia_in)
    return cirugia

@router.delete("/{cirugia_id}", response_model=CirugiaResponse)
def delete_cirugia(
    *,
    db: Session = Depends(get_db),
    cirugia_id: int,
    # current_user = Depends(get_current_active_user)
):
    cirugia = crud_cirugia.get(db, id=cirugia_id)
    if not cirugia:
        raise HTTPException(status_code=404, detail="Cirugia not found")
    cirugia = crud_cirugia.remove(db, id=cirugia_id)
    return cirugia