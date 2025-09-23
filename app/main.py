from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import os

from app.database import engine, Base
from app.routes import (
    clientes, pacientes, 
    consultas, constantes_fisiologicas, estudios, expediente_archivos
)
@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(
    title="Animal-Center API",
    description="API REST para la clinica Veterinaria Animal-Center",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# rutass
# app.include_router(usuarios.router, prefix="/api/v1/usuarios", tags=["usuarios"])
# app.include_router(roles.router, prefix="/api/v1/roles", tags=["roles"])
# app.include_router(permisos.router, prefix="/api/v1/permisos", tags=["permisos"])
app.include_router(clientes.router, prefix="/api/v1/clientes", tags=["clientes"])
app.include_router(pacientes.router, prefix="/api/v1/pacientes", tags=["pacientes"])
app.include_router(consultas.router, prefix="/api/v1/consultas", tags=["consultas"])
app.include_router(constantes_fisiologicas.router, prefix="/api/v1/constantes", tags=["constantes"])
app.include_router(estudios.router, prefix="/api/v1/estudios", tags=["estudios"])

#Rutas Archivos
app.include_router(expediente_archivos.router, prefix="/api/v1/expedientes", tags=["expedientes"])
app.include_router(expediente_archivos.router, prefix="/api/v1/expediente_archivos", tags=["expediente_archivos"])

@app.get("/")
async def root():
    return {"message": "Veterinaria Animal-Center API v1.0.0"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}