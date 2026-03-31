# Variables de entorno

from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Definimos las variables y sus tipos
    app_web_gs_presion: str

    model_config = SettingsConfigDict(env_file=".env")

# Se instancia una sola vez para usarla en toda la aplicación
settings = Settings()
    