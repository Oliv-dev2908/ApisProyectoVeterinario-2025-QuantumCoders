from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.crud.estudios import crud_estudio
from app.schemas.estudios import EstudioCreate, EstudioUpdate, EstudioResponse
# from app.dependencies import get_current_active_user

router = APIRouter()

@router.post("/", response_model=EstudioResponse, status_code=status.HTTP_201_CREATED)
def create_estudio(
    *,
    db: Session = Depends(get_db),
    estudio_in: EstudioCreate,
    # current_user = Depends(get_current_active_user)
):
    estudio = crud_estudio.create(db, obj_in=estudio_in)
    return estudio

@router.get("/", response_model=List[EstudioResponse])
def read_estudios(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    # current_user = Depends(get_current_active_user)
):
    estudios = crud_estudio.get_multi(db, skip=skip, limit=limit)
    return estudios

@router.get("/{estudio_id}", response_model=EstudioResponse)
def read_estudio(
    *,
    db: Session = Depends(get_db),
    estudio_id: int,
    # current_user = Depends(get_current_active_user)
):
    estudio = crud_estudio.get(db, id=estudio_id)
    if not estudio:
        raise HTTPException(status_code=404, detail="Estudio not found")
    return estudio

@router.get("/paciente/{paciente_id}", response_model=List[EstudioResponse])
def read_estudios_by_paciente(
    *,
    db: Session = Depends(get_db),
    paciente_id: int,
    # current_user = Depends(get_current_active_user)
):
    estudios = crud_estudio.get_by_paciente(db, paciente_id=paciente_id)
    return estudios

@router.put("/{estudio_id}", response_model=EstudioResponse)
def update_estudio(
    *,
    db: Session = Depends(get_db),
    estudio_id: int,
    estudio_in: EstudioUpdate,
    # current_user = Depends(get_current_active_user)
):
    estudio = crud_estudio.get(db, id=estudio_id)
    if not estudio:
        raise HTTPException(status_code=404, detail="Estudio not found")
    estudio = crud_estudio.update(db, db_obj=estudio, obj_in=estudio_in)
    return estudio

@router.delete("/{estudio_id}", response_model=EstudioResponse)
def delete_estudio(
    *,
    db: Session = Depends(get_db),
    estudio_id: int,
    # current_user = Depends(get_current_active_user)
):
    estudio = crud_estudio.get(db, id=estudio_id)
    if not estudio:
        raise HTTPException(status_code=404, detail="Estudio not found")
    estudio = crud_estudio.remove(db, id=estudio_id)
    return estudio