from typing import Optional
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from app.crud.base import CRUDBase
from app.models.usuarios import Usuario
from app.schemas.usuarios import UsuarioCreate, UsuarioUpdate

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class CRUDUsuario(CRUDBase[Usuario, UsuarioCreate, UsuarioUpdate]):
    def get_by_email(self, db: Session, *, email: str) -> Optional[Usuario]:
        return db.query(Usuario).filter(Usuario.email == email).first()

    def create(self, db: Session, *, obj_in: UsuarioCreate) -> Usuario:
        hashed_password = pwd_context.hash(obj_in.contraseña)
        db_obj = Usuario(
            nombre=obj_in.nombre,
            email=obj_in.email,
            contraseña_hash=hashed_password,
            rol_id=obj_in.rol_id,
            activo=obj_in.activo,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def authenticate(self, db: Session, *, email: str, password: str) -> Optional[Usuario]:
        user = self.get_by_email(db, email=email)
        if not user:
            return None
        if not pwd_context.verify(password, user.contraseña_hash):
            return None
        return user

    def get(self, db: Session, id: int) -> Optional[Usuario]:
        return db.query(self.model).filter(self.model.id_usuario == id).first()

    def get_multi(self, db: Session, *, skip: int = 0, limit: int = 100):
        return db.query(self.model).offset(skip).limit(limit).all()

    def remove(self, db: Session, *, id: int) -> Usuario:
        obj = db.query(self.model).filter(self.model.id_usuario == id).first()
        db.delete(obj)
        db.commit()
        return obj

crud_usuario = CRUDUsuario(Usuario)