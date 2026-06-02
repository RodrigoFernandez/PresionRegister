# AGENTS.md

Contexto operativo y reglas para cualquier agente que trabaje en este repositorio.

## Resumen del proyecto

**PresionRegister** es una API personal para registrar presión arterial (sistólica, diastólica, pulso). Los datos se reenvían a un Google Apps Script Web App, que es el encargado de persistir las mediciones en una hoja de Google Sheets. La API no maneja credenciales de Google ni base de datos propia.

## Stack

- Python ≥ 3.12
- FastAPI (servidor HTTP)
- Uvicorn (ASGI server)
- pydantic-settings (configuración por variables de entorno)
- httpx (cliente HTTP asíncrono hacia Apps Script)
- uv (gestor de dependencias y entorno virtual)

## Comandos

```bash
# Instalar / sincronizar dependencias
uv sync

# Levantar la app en desarrollo (recarga automática)
uv run uvicorn main:app --reload

# Build y ejecución con Docker
docker build -t presionregister .
docker run --rm -p 8000:8000 --env-file .env presionregister
```

No hay suite de tests ni linter configurados. Si el usuario pide agregar tests, usar `pytest` + `httpx.MockTransport` y `pytest-asyncio`.

## Variables de entorno

Definidas en `.env` (ignorado por git). Carga gestionada por `pydantic-settings` en `src/presionregister/config.py`.

| Variable | Tipo | Descripción |
|---|---|---|
| `app_web_gs_presion` | `str` | URL del Web App desplegado en Google Apps Script. Endpoint al que se reenvía cada registro. |

## Estructura del repositorio

```
.
├── main.py                       # App FastAPI y endpoints
├── pyproject.toml                # Dependencias y metadata
├── uv.lock                       # Lockfile de uv (no editar a mano)
├── Dockerfile                    # Imagen de producción
├── .env                          # Variables de entorno (NO commitear)
├── .gitignore                    # Ignora .env
└── src/presionregister/
    ├── __init__.py
    ├── config.py                 # Settings (pydantic-settings)
    ├── logger.py                 # Logger `presion_register` a stdout
    ├── models.py                 # Esquemas Pydantic (request/response)
    └── spreadsheet.py            # Cliente GoogleSheetManager (httpx)
```

## API expuesta

### `GET /`
Devuelve un mensaje de bienvenida. Útil como healthcheck.

### `POST /registro`
Registra una medición de presión.

**Request body** (`RegistroPresion`):
```json
{
  "sistolica": 120,
  "diastolica": 80,
  "pulso": 70
}
```

**Response 200** (`RespuestaRegistro`):
```json
{
  "status": "success",
  "mensaje": "Registro exitoso"
}
```

**Response 500**: falla al inicializar el cliente de Google Sheets o al reenviar el registro. Se loggea la causa.

> **Nota**: `fecha` y `hora` no las envía el cliente. Las genera el servidor en `spreadsheet.py` con `datetime.now()` para uniformidad entre registros.

## Validaciones

Definidas en `src/presionregister/models.py`:

- `sistolica`, `diastolica`, `pulso`: `int` en rango `0 ≤ x ≤ 250`
- `PresionRegister.fecha`: `str` con regex `^\d{4}-\d{2}-\d{2}$`
- `PresionRegister.hora`: `str` con regex `^\d{2}:\d{2}:\d{2}$`

## Reglas operativas

1. **No commitear sin confirmación explícita** del usuario. Nunca usar `git commit` proactivamente.
2. **No exponer ni commitear `.env`**. El archivo ya está en `.gitignore`.
3. **Gestionar dependencias sólo con `uv add` / `uv remove`**. No editar `pyproject.toml` ni `uv.lock` a mano.
4. **Mensajes, logs y comentarios de documentación en español**. El código (identificadores, docstrings) en español o inglés, consistente con el archivo.
5. **Sin comentarios superfluos en el código**. No agregar comentarios que repitan lo evidente.
6. **Errores HTTP** siempre con `HTTPException(status_code=..., detail=...)`. Loggear antes de lanzar.
7. **Cliente HTTP** siempre con `httpx.AsyncClient` y `follow_redirects=True` (Apps Script puede redirigir).
8. **No agregar features fuera de alcance**: registro personal de presión arterial. No añadir autenticación, multiusuario, persistencia local, etc. sin pedido explícito.
9. **No instalar paquetes nuevos** salvo pedido explícito del usuario.
10. **Una sola fuente de verdad** para configuración: `settings = Settings()` en `config.py`.

## Pendientes conocidos

- Sin tests automatizados.
- Sin CI/CD.
- Sin rate limiting ni autenticación (uso personal, expuesto en local/red doméstica).
- El timestamp lo genera el servidor; si en el futuro el cliente debe enviarlo, ajustar `models.py` y `spreadsheet.py` en conjunto.
