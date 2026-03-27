# Esquemas de Pydantic

from pydantic import BaseModel, Field
#from datetime import datetime

class PresionRegister(BaseModel):
    sistolica: int = Field(..., ge=0, le=250)
    diastolica: int = Field(..., ge=0, le=250)
    pulso: int = Field(..., ge=0, le=250)
    #fecha_hora: datetime = Field(default_factory=datetime.now )
    fecha: str = Field(..., pattern=r"^\d{4}-\d{2}-\d{2}$")
    hora: str = Field(..., pattern=r"^\d{2}:\d{2}:\d{2}$")

class RegistroPresion(BaseModel):
    sistolica: int = Field(..., ge=0, le=250, description="Presión sistólica")
    diastolica: int = Field(..., ge=0, le=250, description="Presión diastólica")
    pulso: int = Field(..., ge=0, le=250, description="Pulso")

class RespuestaRegistro(BaseModel):
    status: str
    mensaje: str
    