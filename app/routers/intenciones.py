from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas
from app.services.match import verificar_y_crear_match
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer
import os

router = APIRouter(prefix="/intenciones", tags=["Intenciones"])

# Esquema de seguridad para extraer el token JWT
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/usuarios/login")

# Función para obtener el usuario actual desde el token
def obtener_usuario_actual(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> models.Usuario:
    try:
        payload = jwt.decode(
            token,
            os.getenv("SECRET_KEY"),
            algorithms=[os.getenv("ALGORITHM")]
        )
        usuario_id = int(payload.get("sub"))
    except (JWTError, TypeError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado"
        )

    usuario = db.query(models.Usuario).filter(
        models.Usuario.id == usuario_id
    ).first()

    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )

    return usuario

# Endpoint para enviar una intención
@router.post("/enviar", status_code=201)
def enviar_intencion(
    datos: schemas.IntencionCrear,
    db: Session = Depends(get_db),
    usuario_actual: models.Usuario = Depends(obtener_usuario_actual)
):
    # No puedes enviarte una intención a ti mismo
    if datos.usuario_destino_id == usuario_actual.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No puedes enviarte una intención a ti mismo"
        )

    # Verificamos que el usuario destino existe
    destino = db.query(models.Usuario).filter(
        models.Usuario.id == datos.usuario_destino_id
    ).first()

    if not destino:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario destino no encontrado"
        )

    # Verificamos que no exista ya esta intención
    intencion_existente = db.query(models.Intencion).filter(
        models.Intencion.usuario_origen_id == usuario_actual.id,
        models.Intencion.usuario_destino_id == datos.usuario_destino_id,
        models.Intencion.tipo_intencion_id == datos.tipo_intencion_id
    ).first()

    if intencion_existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ya enviaste esta intención a este usuario"
        )

    # Guardamos la intención
    nueva_intencion = models.Intencion(
        usuario_origen_id=usuario_actual.id,
        usuario_destino_id=datos.usuario_destino_id,
        tipo_intencion_id=datos.tipo_intencion_id
    )

    db.add(nueva_intencion)
    db.commit()
    db.refresh(nueva_intencion)

    # Activamos la compuerta AND
    match = verificar_y_crear_match(
        db=db,
        usuario_origen_id=usuario_actual.id,
        usuario_destino_id=datos.usuario_destino_id,
        tipo_intencion_id=datos.tipo_intencion_id
    )

    # Si hay match, lo notificamos. Si no, silencio total.
    if match:
        return {
            "mensaje": "¡Es un match! 🎉",
            "match": {
                "id": match.id,
                "usuario_a_id": match.usuario_a_id,
                "usuario_b_id": match.usuario_b_id,
                "tipo_intencion_id": match.tipo_intencion_id,
                "fecha_match": match.fecha_match
            }
        }

    return {"mensaje": "Intención enviada"}