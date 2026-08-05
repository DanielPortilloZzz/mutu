from pydantic import BaseModel, EmailStr
from datetime import datetime

# --- Esquemas de Usuario ---

class UsuarioCrear(BaseModel):
    nombre: str
    email: EmailStr
    contraseña: str

class UsuarioRespuesta(BaseModel):
    id: int
    nombre: str
    email: str
    fecha_registro: datetime

    class Config:
        from_attributes = True

class LoginDatos(BaseModel):
    email: EmailStr
    contraseña: str

class TokenRespuesta(BaseModel):
    access_token: str
    token_type: str

# --- Esquemas de Intenciones ---

class IntencionCrear(BaseModel):
    usuario_destino_id: int
    tipo_intencion_id: int

class IntencionRespuesta(BaseModel):
    id: int
    usuario_origen_id: int
    usuario_destino_id: int
    tipo_intencion_id: int
    fecha_envio: datetime

    class Config:
        from_attributes = True

# --- Esquemas de Match ---

class MatchRespuesta(BaseModel):
    id: int
    usuario_a_id: int
    usuario_b_id: int
    tipo_intencion_id: int
    fecha_match: datetime

    class Config:
        from_attributes = True