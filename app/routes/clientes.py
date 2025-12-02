from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.crud.clientes import crud_cliente
from app.schemas.clientes import ClienteCreate, ClienteUpdate, ClienteResponse
# from app.dependencies import get_current_active_user

router = APIRouter()

@router.post("/", response_model=ClienteResponse, status_code=status.HTTP_201_CREATED)
def create_cliente(
    *,
    db: Session = Depends(get_db),
    cliente_in: ClienteCreate,
    # current_user = Depends(get_current_active_user)
):
    cliente = crud_cliente.create(db, obj_in=cliente_in)
    return cliente

@router.get("/", response_model=List[ClienteResponse])
def read_clientes(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 500,
    # current_user = Depends(get_current_active_user)
):
    clientes = crud_cliente.get_multi(db, skip=skip, limit=limit)
    return clientes

@router.get("/{cliente_id}", response_model=ClienteResponse)
def read_cliente(
    *,
    db: Session = Depends(get_db),
    cliente_id: int,
    # current_user = Depends(get_current_active_user)
):
    cliente = crud_cliente.get(db, id=cliente_id)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente not found")
    return cliente

@router.put("/{cliente_id}", response_model=ClienteResponse)
def update_cliente(
    *,
    db: Session = Depends(get_db),
    cliente_id: int,
    cliente_in: ClienteUpdate,
    # current_user = Depends(get_current_active_user)
):
    cliente = crud_cliente.get(db, id=cliente_id)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente not found")
    cliente = crud_cliente.update(db, db_obj=cliente, obj_in=cliente_in)
    return cliente

@router.delete("/{cliente_id}", response_model=ClienteResponse)
def delete_cliente(
    *,
    db: Session = Depends(get_db),
    cliente_id: int,
    # current_user = Depends(get_current_active_user)
):
    cliente = crud_cliente.get(db, id=cliente_id)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente not found")
    cliente = crud_cliente.remove(db, id=cliente_id)
    return cliente