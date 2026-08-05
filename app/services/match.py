from sqlalchemy.orm import Session
from app import models
from datetime import datetime, timezone

def verificar_y_crear_match(
    db: Session,
    usuario_origen_id: int,
    usuario_destino_id: int,
    tipo_intencion_id: int
) -> models.Match | None:
    """
    Aquí vive la compuerta AND de Mutu.
    Busca si ya existe una intención inversa.
    Si existe, crea el match y lo devuelve.
    Si no existe, devuelve None silenciosamente.
    """

    # Buscamos si el destino ya envió la misma intención al origen
    intencion_inversa = db.query(models.Intencion).filter(
        models.Intencion.usuario_origen_id == usuario_destino_id,
        models.Intencion.usuario_destino_id == usuario_origen_id,
        models.Intencion.tipo_intencion_id == tipo_intencion_id
    ).first()

    # Si no hay intención inversa, silencio total
    if not intencion_inversa:
        return None

    # Si hay coincidencia, creamos el match
    nuevo_match = models.Match(
        usuario_a_id=usuario_origen_id,
        usuario_b_id=usuario_destino_id,
        tipo_intencion_id=tipo_intencion_id,
        fecha_match=datetime.now(timezone.utc)
    )

    db.add(nuevo_match)
    db.commit()
    db.refresh(nuevo_match)

    return nuevo_match