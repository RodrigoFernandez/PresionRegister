# Principal

from fastapi import FastAPI
from src.presionregister.models import RegistroPresion, RespuestaRegistro
from src.config import settings
from src.logger import log
from src.spreadsheet import iniciar_cliente_google_sheets


app = FastAPI(
    title="Registro de Presión Arterial Personal",
    description="API para el registro de presión arterial personal",
    version="0.1.0"
)

# Inicilización del cliente de google sheets
gs_client = iniciar_cliente_google_sheets(settings)

@app.get("/")
async def root():
    return {"message": "Bienvenido al registro de presión arterial personal"}

@app.post("/registro", response_model=RespuestaRegistro)
async def registro(registro: RegistroPresion):
    print(registro)

    if not gs_client:
        log.error("Error al inicializar el cliente de google sheets")
        #return RespuestaRegistro(status="error", mensaje="Error al inicializar el cliente de google sheets")
        raise HTTPException(status_code=500, detail="Error al inicializar el cliente de google sheets")

    try:
        await gs_client.agregar_registro(registro)
        log.info(f"Registro exitoso: {registro}")
        return RespuestaRegistro(status="success", mensaje="Registro exitoso")
    except Exception as e:
        log.exception(f"Error al registrar: {e}")
        #return RespuestaRegistro(status="error", mensaje=f"Error al registrar: {e}")
        raise HTTPException(status_code=500, detail=f"Error al registrar: {e}")

