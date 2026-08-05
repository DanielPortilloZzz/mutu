from fastapi import FastAPI
from app.database import engine, Base
from app.routers import usuarios, intenciones

app = FastAPI(
    title="Mutu API",
    description="API para la app de conexión social Mutu",
    version="0.1.0"
)

Base.metadata.create_all(bind=engine)

app.include_router(usuarios.router)
app.include_router(intenciones.router)

@app.get("/")
def root():
    return {"mensaje": "Mutu API funcionando ✅"}