# ARCHITECTURE.md

Diseño y flujo de datos de PresionRegister.

## Visión general

API personal de registro de presión arterial. El backend **no persiste datos**: delega la escritura a un Google Apps Script Web App, que es el único que habla con Google Sheets. Esto evita manejar credenciales de Google,OAuth o service accounts en el servidor.

## Diagrama de flujo

```
┌──────────┐  POST /registro   ┌────────────────────┐
│ Cliente  │ ────────────────▶ │   FastAPI (main)   │
└──────────┘   {sistolica,      │   - valida body    │
              diastolica,      │   - genera fecha/  │
              pulso}           │     hora server    │
                              └─────────┬──────────┘
                                        │
                                        ▼
                              ┌────────────────────┐
                              │ GoogleSheetManager │
                              │  (spreadsheet.py)  │
                              │  httpx.AsyncClient │
                              └─────────┬──────────┘
                                        │  POST JSON
                                        │  {fecha, hora,
                                        │   sistolica,
                                        │   diastolica,
                                        │   pulso}
                                        ▼
                              ┌────────────────────┐
                              │  Apps Script       │
                              │  Web App (externo) │
                              └─────────┬──────────┘
                                        ▼
                              ┌────────────────────┐
                              │  Google Sheets     │
                              │  (persistencia)    │
                              └────────────────────┘
```

## Capas

| Capa | Módulo | Responsabilidad |
|---|---|---|
| HTTP | `main.py` | Routing, validación de entrada, traducción de excepciones, formato de respuesta. |
| Dominio | `src/presionregister/models.py` | Esquemas Pydantic: `RegistroPresion` (entrada), `RespuestaRegistro` (salida), `PresionRegister` (interno, incluye fecha/hora). |
| Integración | `src/presionregister/spreadsheet.py` | Cliente HTTP hacia el Apps Script. Encapsula URL, payload y manejo de respuesta. |
| Soporte | `src/presionregister/config.py` | Carga de variables de entorno vía `pydantic-settings`. |
| Soporte | `src/presionregister/logger.py` | Logger singleton `presion_register` con salida a stdout. |

## Decisiones de diseño

### Persistencia delegada al Apps Script
La API no escribe directamente en Google Sheets. Razones:
- No hay que manejar credenciales de Google en el servidor.
- El Apps Script puede evolucionar (validaciones, formato, triggers) sin redeploy de la API.
- La API queda como un proxy tonto y validado.

### Timestamp generado en el servidor
`fecha` y `hora` los produce `spreadsheet.py` con `datetime.now()`. Razones:
- Uniformidad de zona horaria (la del servidor).
- El cliente no necesita enviar timestamp; menos campos = menos errores.
- Si en el futuro se necesita zona del cliente, se ajusta el modelo `PresionRegister` y se propaga.

### Una sola variable de entorno
`app_web_gs_presion` es la URL del Web App desplegado. Sin secretos adicionales (el Apps Script está publicado para acceso anónimo o con la protección que el propio script defina).

### `httpx.AsyncClient` con `follow_redirects=True`
Apps Script puede responder con redirecciones. La flag evita falsos errores 3xx en producción.

### Sin autenticación
Uso personal. La API se expone en la red local. Si en el futuro se publica a internet, agregar API key o autenticación por token como middleware de FastAPI.

## Modelo de despliegue

- **Imagen base**: `python:3.12-slim`.
- **Gestor de paquetes dentro del contenedor**: `uv` (copiado desde `ghcr.io/astral-sh/uv`).
- **Síncronización**: `uv sync --frozen` para usar el `uv.lock` exacto.
- **Comando de arranque**: `uv run uvicorn main:app --host 0.0.0.0 --port 8000 --workers 1`.
- **Recursos**: 1 worker (carga mínima personal).

## Puntos de extensión

Si el proyecto crece, los siguientes puntos están preparados para extenderse sin reescritura:

1. **Agregar campos al registro** (ej. `brazo`, `posicion`): extender `RegistroPresion` y `PresionRegister`, ajustar `spreadsheet.py` y el Apps Script.
2. **Múltiples destinos de persistencia**: convertir `GoogleSheetManager` en interfaz y agregar implementaciones (SQLite, InfluxDB, etc.).
3. **GET /registros**: nuevo endpoint que llame a un método `obtener_registros` en `GoogleSheetManager`.
4. **Autenticación**: middleware de FastAPI que valide header/cookie; el resto de la app no se entera.
