from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.database import Base

# Modelo de la tabla usuarios
class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, nullable=False)
    contraseña = Column(String(255), nullable=False)
    fecha_registro = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Relaciones
    intenciones_enviadas = relationship("Intencion", foreign_keys="Intencion.usuario_origen_id", back_populates="origen")
    intenciones_recibidas = relationship("Intencion", foreign_keys="Intencion.usuario_destino_id", back_populates="destino")

# Modelo del catálogo de tipos de intención
class IntencionesCatalogo(Base):
    __tablename__ = "intenciones_catalogo"

    id = Column(Integer, primary_key=True, index=True)
    descripcion = Column(String(100), nullable=False, unique=True)

# Modelo de la tabla intenciones (corazón de Mutu)
class Intencion(Base):
    __tablename__ = "intenciones"

    id = Column(Integer, primary_key=True, index=True)
    usuario_origen_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    usuario_destino_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    tipo_intencion_id = Column(Integer, ForeignKey("intenciones_catalogo.id"), nullable=False)
    fecha_envio = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Relaciones
    origen = relationship("Usuario", foreign_keys=[usuario_origen_id], back_populates="intenciones_enviadas")
    destino = relationship("Usuario", foreign_keys=[usuario_destino_id], back_populates="intenciones_recibidas")
    catalogo = relationship("IntencionesCatalogo")

    # Restricción: un usuario no puede enviar la misma intención dos veces al mismo destino
    __table_args__ = (
        UniqueConstraint("usuario_origen_id", "usuario_destino_id", "tipo_intencion_id"),
    )

# Modelo de la tabla matches
class Match(Base):
    __tablename__ = "matches"

    id = Column(Integer, primary_key=True, index=True)
    usuario_a_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    usuario_b_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    tipo_intencion_id = Column(Integer, ForeignKey("intenciones_catalogo.id"), nullable=False)
    fecha_match = Column(DateTime, default=lambda: datetime.now(timezone.utc))