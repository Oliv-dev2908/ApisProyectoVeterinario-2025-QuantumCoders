from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.crud.fases_tratamiento import crud_fase_tratamiento
from app.schemas.fases_tratamiento import FaseTratamientoCreate, FaseTratamientoUpdate, FaseTratamientoResponse

router = APIRouter()

@router.post("/", response_model=FaseTratamientoResponse, status_code=status.HTTP_201_CREATED)
def create_fase_tratamiento(
    *,
    db: Session = Depends(get_db),
    fase_in: FaseTratamientoCreate
):
    fase = crud_fase_tratamiento.create(db, obj_in=fase_in)
    crud_fase_tratamiento.add_price_tratamiento(fase.costo, db, fase.id_tratamiento)
    return fase


@router.get("/tratamiento/{tratamiento_id}", response_model=List[FaseTratamientoResponse])
def read_fases_por_tratamiento(
    tratamiento_id: int,
    db: Session = Depends(get_db)
):
    fases = crud_fase_tratamiento.get_by_tratamiento(db, tratamiento_id)
    return fases
@router.put("/{fase_tratamiento_id}", response_model=FaseTratamientoResponse)
def update_fase_tratamiento(
    *,
    db: Session = Depends(get_db),
    fase_tratamiento_id: int,
    fase_tratamiento_in: FaseTratamientoUpdate,
):
    fase_tratamiento = crud_fase_tratamiento.get_by_id_fase(db, id_fase=fase_tratamiento_id)
    if not fase_tratamiento:
        raise HTTPException(status_code=404, detail="Tratamiento not found")
    
    costo_anterior = fase_tratamiento.costo 

    fase_actualizada = crud_fase_tratamiento.update(db, db_obj=fase_tratamiento, obj_in=fase_tratamiento_in)

    diferencia = fase_actualizada.costo - costo_anterior
    if diferencia != 0:
        crud_fase_tratamiento.add_price_tratamiento(diferencia, db, fase_actualizada.id_tratamiento)

    return fase_actualizada

@router.delete("/{fase_tratamiento_id}", response_model=FaseTratamientoResponse)
def delete_tratamiento(
    *,
    db: Session = Depends(get_db),
    fase_tratamiento_id: int,
):
    fase_tratamiento = crud_fase_tratamiento.get_by_id_fase(db, id_fase=fase_tratamiento_id)
    if not fase_tratamiento:
        raise HTTPException(status_code=404, detail="Fase not found")
    crud_fase_tratamiento.add_price_tratamiento((fase_tratamiento.costo) * (-1), db, fase_tratamiento.id_tratamiento)
    fase_tratamiento = crud_fase_tratamiento.remove(db, id=fase_tratamiento_id)
    return fase_tratamiento
