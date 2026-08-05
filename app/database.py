# Importamos las herramientas necesarias de SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

# Cargamos las variables del archivo .env
load_dotenv()

# Leemos la URL de conexión a PostgreSQL
DATABASE_URL = os.getenv("DATABASE_URL")

# Creamos el motor de conexión a la base de datos
engine = create_engine(DATABASE_URL)

# Creamos la sesión para interactuar con la base de datos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base de la que heredarán todos los modelos
Base = declarative_base()

# Función que provee una sesión por cada petición
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()