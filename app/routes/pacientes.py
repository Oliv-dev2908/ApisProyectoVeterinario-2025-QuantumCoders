from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.crud.pacientes import crud_paciente
from app.schemas.pacientes import PacienteCreate, PacienteUpdate, PacienteResponse
# from app.dependencies import get_current_active_user

router = APIRouter()

@router.post("/", response_model=PacienteResponse, status_code=status.HTTP_201_CREATED)
def create_paciente(
    *,
    db: Session = Depends(get_db),
    paciente_in: PacienteCreate,
    # current_user = Depends(get_current_active_user)
):
    paciente = crud_paciente.create(db, obj_in=paciente_in)
    return paciente

@router.get("/", response_model=List[PacienteResponse])
def read_pacientes(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 500,
    # current_user = Depends(get_current_active_user)
):
    pacientes = crud_paciente.get_multi(db, skip=skip, limit=limit)
    return pacientes

@router.get("/{paciente_id}", response_model=PacienteResponse)
def read_paciente(
    *,
    db: Session = Depends(get_db),
    paciente_id: int,
    # current_user = Depends(get_current_active_user)
):
    paciente = crud_paciente.get(db, id=paciente_id)
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente not found")
    return paciente

@router.get("/cliente/{cliente_id}", response_model=List[PacienteResponse])
def read_pacientes_by_cliente(
    *,
    db: Session = Depends(get_db),
    cliente_id: int,
    # current_user = Depends(get_current_active_user)
):
    pacientes = crud_paciente.get_by_cliente(db, cliente_id=cliente_id)
    return pacientes

@router.put("/{paciente_id}", response_model=PacienteResponse)
def update_paciente(
    *,
    db: Session = Depends(get_db),
    paciente_id: int,
    paciente_in: PacienteUpdate,
    # current_user = Depends(get_current_active_user)
):
    paciente = crud_paciente.get(db, id=paciente_id)
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente not found")
    paciente = crud_paciente.update(db, db_obj=paciente, obj_in=paciente_in)
    return paciente

@router.delete("/{paciente_id}", response_model=PacienteResponse)
def delete_paciente(
    *,
    db: Session = Depends(get_db),
    paciente_id: int,
    # current_user = Depends(get_current_active_user)
):
    paciente = crud_paciente.get(db, id=paciente_id)
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente not found")
    paciente = crud_paciente.remove(db, id=paciente_id)
    return paciente
