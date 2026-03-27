# Principal

from fastapi import FastAPI
from src.presionregister.models import RegistroPresion, RespuestaRegistro

app = FastAPI(
    title="Registro de Presión Arterial Personal",
    description="API para el registro de presión arterial personal",
    version="0.1.0"
)

@app.get("/")
async def root():
    return {"message": "Bienvenido al registro de presión arterial personal"}

@app.post("/registro", response_model=RespuestaRegistro)
async def registro(registro: RegistroPresion):
    print(registro)
    return RespuestaRegistro(status="success", mensaje="Registro exitoso")

