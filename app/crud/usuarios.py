from sqlalchemy.orm import Session
from fastapi import HTTPException
from app import models, schemas
from datetime import datetime


class CRUDUsuario:

    # 🔹 Listar usuarios
    def get_usuarios(self, db: Session, skip: int = 0, limit: int = 100):
        return db.query(models.usuarios.Usuario).offset(skip).limit(limit).all()

# 🔹 Obtener un usuario por ID
    def get_usuario(self, db: Session, usuario_id: int):
        usuario = db.query(models.usuarios.Usuario).filter(models.usuarios.Usuario.id_usuario == usuario_id).first()
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        return usuario

# 🔹 Crear usuario
    def create_usuario(self, db: Session, usuario: schemas.usuarios.UsuarioCreate):
        db_usuario = models.usuarios.Usuario(
            nombre=usuario.nombre,
            email=usuario.email,
            rol_id=usuario.rol_id,
            activo=usuario.activo,
            supabase_user_id=usuario.supabase_user_id,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        db.add(db_usuario)
        db.commit()
        db.refresh(db_usuario)
        return db_usuario

# 🔹 Actualizar usuario
    def update_usuario(self, db: Session, usuario_id: int, usuario: schemas.usuarios.UsuarioUpdate):
        db_usuario = db.query(models.usuarios.Usuario).filter(models.usuarios.Usuario.id_usuario == usuario_id).first()
        if not db_usuario:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")

        db_usuario.nombre = usuario.nombre
        db_usuario.email = usuario.email
        db_usuario.rol_id = usuario.rol_id
        db_usuario.activo = usuario.activo
        db_usuario.updated_at = datetime.utcnow()

        db.commit()
        db.refresh(db_usuario)
        return db_usuario

# 🔹 Eliminar usuario
    def delete_usuario(self, db: Session, usuario_id: int):
        db_usuario = db.query(models.usuarios.Usuario).filter(models.usuarios.Usuario.id_usuario == usuario_id).first()
        if not db_usuario:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")

        db.delete(db_usuario)
        db.commit()
        return {"message": "Usuario eliminado correctamente"}

crud_usuario = CRUDUsuario()