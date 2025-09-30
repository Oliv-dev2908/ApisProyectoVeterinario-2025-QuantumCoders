from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
from app.database import get_db
from app import schemas
from app.crud.usuarios import crud_usuario  # 👈 importa la instancia correcta

router = APIRouter()

@router.get("/", response_model=List[schemas.UsuarioResponse])
def listar_usuarios(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud_usuario.get_usuarios(db, skip, limit)

@router.get("/{supabase_user_id}", response_model=schemas.UsuarioResponse)
def obtener_usuario(supabase_user_id: UUID, db: Session = Depends(get_db)):
    return crud_usuario.get_usuario(db, supabase_user_id)

@router.post("/", response_model=schemas.UsuarioResponse)
def crear_usuario(usuario: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    return crud_usuario.create_usuario(db, usuario)

@router.put("/{supabase_user_id}", response_model=schemas.UsuarioResponse)
def actualizar_usuario(supabase_user_id: UUID, usuario: schemas.UsuarioUpdate, db: Session = Depends(get_db)):
    return crud_usuario.update_usuario(db, supabase_user_id, usuario)

@router.delete("/{supabase_user_id}")
def eliminar_usuario(supabase_user_id: UUID, db: Session = Depends(get_db)):
    return crud_usuario.delete_usuario(db, supabase_user_id)