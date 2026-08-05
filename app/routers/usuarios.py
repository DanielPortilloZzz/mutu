from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta, timezone
import os

# Configuración del router
router = APIRouter(prefix="/usuarios", tags=["Usuarios"])

# Configuración de encriptación de contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Función para encriptar contraseña
def encriptar_contraseña(contraseña: str) -> str:
    return pwd_context.hash(contraseña)

# Función para verificar contraseña
def verificar_contraseña(contraseña_plana: str, contraseña_hash: str) -> bool:
    return pwd_context.verify(contraseña_plana, contraseña_hash)

# Función para crear el token JWT
def crear_token(data: dict) -> str:
    datos = data.copy()
    expiracion = datetime.now(timezone.utc) + timedelta(
        minutes=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
    )
    datos.update({"exp": expiracion})
    return jwt.encode(datos, os.getenv("SECRET_KEY"), algorithm=os.getenv("ALGORITHM"))

# Endpoint de registro
@router.post("/registro", response_model=schemas.UsuarioRespuesta, status_code=201)
def registrar_usuario(datos: schemas.UsuarioCrear, db: Session = Depends(get_db)):
    # Verificamos si el email ya existe
    usuario_existente = db.query(models.Usuario).filter(
        models.Usuario.email == datos.email
    ).first()

    if usuario_existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El email ya está registrado"
        )

    # Creamos el nuevo usuario con la contraseña encriptada
    nuevo_usuario = models.Usuario(
        nombre=datos.nombre,
        email=datos.email,
        contraseña=encriptar_contraseña(datos.contraseña)
    )

    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)

    return nuevo_usuario

# Endpoint de login
@router.post("/login", response_model=schemas.TokenRespuesta)
def login(datos: schemas.LoginDatos, db: Session = Depends(get_db)):
    # Buscamos el usuario por email
    usuario = db.query(models.Usuario).filter(
        models.Usuario.email == datos.email
    ).first()

    # Verificamos que exista y que la contraseña sea correcta
    if not usuario or not verificar_contraseña(datos.contraseña, usuario.contraseña):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email o contraseña incorrectos"
        )

    # Generamos el token JWT
    token = crear_token({"sub": str(usuario.id)})

    return {"access_token": token, "token_type": "bearer"}