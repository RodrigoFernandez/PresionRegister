# Lógica de gspread
from .models import PresionRegister
from .logger import log
import httpx
from datetime import datetime

class GoogleSheetManager:
    def __init__(self, web_app_url: str):
        self.url = web_app_url

    async def agregar_registro(self, datos: PresionRegister):

        ahora = datetime.now()


        # Preparamos el payload con el formato exacto de las columnas
        payload = {
            "fecha": f"{ahora.date()}",
            "hora": ahora.strftime("%H:%M"),
            "sistolica": datos.sistolica,
            "diastolica": datos.diastolica,
            "pulso": datos.pulso
        }
        
        async with httpx.AsyncClient(follow_redirects=True) as cliente:
            response = await cliente.post(self.url, json=payload)

            if response.status_code != 200:
                log.error(f"Error al agregar registro: {response.status_code} - {response.text}")
                raise Exception(f"Error al agregar registro")
            
            return response.json()
            

def iniciar_cliente_google_sheets(settings):
    try:
        return GoogleSheetManager(
            web_app_url=settings.app_web_gs_presion
        )
    except Exception as e:
        print(f"Error al inicializar el cliente de google sheets: {e}")
        log.error(f"Error al inicializar el cliente de google sheets: {e}")
        return None     

    
        