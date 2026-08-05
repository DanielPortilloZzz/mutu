# Mutu 🤝

App de conexión social cuyo concepto central es eliminar el miedo al rechazo en las interacciones humanas cotidianas.

## ¿Cómo funciona?

El usuario A puede enviar una "intención" al usuario B (por ejemplo: "Me gustas"), pero esa intención permanece completamente invisible para el usuario B a menos que B haya enviado exactamente la misma intención a A de forma independiente.

Solo cuando ambas intenciones existen mutuamente, los dos usuarios reciben la notificación al mismo tiempo. Funciona como una compuerta lógica AND.

## Tecnologías

- **Python 3.14** + **FastAPI** → API REST
- **PostgreSQL** → Base de datos
- **SQLAlchemy** → ORM
- **JWT** → Autenticación
- **bcrypt** → Encriptación de contraseñas

## Instalación

1. Clonar el repositorio

        git clone https://github.com/DanielPortilloZzz/mutu.git
        cd mutu

2. Crear y activar el entorno virtual

        python -m venv venv
        venv\Scripts\activate

3. Instalar dependencias

        pip install -r requirements.txt
        pip install "pydantic[email]"

4. Crear un archivo .env en la raíz con este contenido

        DATABASE_URL=postgresql://postgres:tu_contraseña@localhost:5432/mutu_db
        SECRET_KEY=tu_clave_secreta
        ALGORITHM=HS256
        ACCESS_TOKEN_EXPIRE_MINUTES=30

5. Crear la base de datos en PostgreSQL

        CREATE DATABASE mutu_db;

6. Arrancar el servidor

        uvicorn app.main:app --reload

7. Ver la documentación en el navegador

        http://127.0.0.1:8000/docs

## Endpoints disponibles

| Método | Endpoint | Descripción |
|---|---|---|
| POST | /usuarios/registro | Registrar nuevo usuario |
| POST | /usuarios/login | Iniciar sesión |
| POST | /intenciones/enviar | Enviar una intención |

## Filosofía de diseño

Esta app no debe ser adictiva. Está prohibido:

- Scroll infinito
- Notificaciones agresivas
- Métricas de vanidad

El objetivo es que las personas se conozcan en el mundo real.

## Estado del proyecto

En desarrollo activo — MVP en construcción