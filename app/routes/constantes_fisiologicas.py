from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.crud.constantes import crud_constante
from app.schemas.constantes import ConstanteCreate, ConstanteUpdate, ConstanteResponse
# from app.dependencies import get_current_active_user

router = APIRouter()

@router.post("/", response_model=ConstanteResponse, status_code=status.HTTP_201_CREATED)
def create_constante(
    *,
    db: Session = Depends(get_db),
    constante_in: ConstanteCreate,
    # current_user = Depends(get_current_active_user)
):
    constante = crud_constante.create(db, obj_in=constante_in)
    return constante

@router.get("/", response_model=List[ConstanteResponse])
def read_constantes(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    # current_user = Depends(get_current_active_user)
):
    constantes = crud_constante.get_multi(db, skip=skip, limit=limit)
    return constantes

@router.get("/{consulta_id}", response_model=ConstanteResponse)
def read_constante(
    *,
    db: Session = Depends(get_db),
    consulta_id: int,
    # current_user = Depends(get_current_active_user)
):
    constante = crud_constante.get(db, id=consulta_id)
    if not constante:
        raise HTTPException(status_code=404, detail="Constante fisiológica not found")
    return constante

@router.put("/{consulta_id}", response_model=ConstanteResponse)
def update_constante(
    *,
    db: Session = Depends(get_db),
    consulta_id: int,
    constante_in: ConstanteUpdate,
    # current_user = Depends(get_current_active_user)
):
    constante = crud_constante.get(db, id=consulta_id)
    if not constante:
        raise HTTPException(status_code=404, detail="Constante fisiológica not found")
    constante = crud_constante.update(db, db_obj=constante, obj_in=constante_in)
    return constante

@router.delete("/{consulta_id}", response_model=ConstanteResponse)
def delete_constante(
    *,
    db: Session = Depends(get_db),
    consulta_id: int,
    # current_user = Depends(get_current_active_user)
):
    constante = crud_constante.get(db, id=consulta_id)
    if not constante:
        raise HTTPException(status_code=404, detail="Constante fisiológica not found")
    constante = crud_constante.remove(db, id=consulta_id)
    return constante