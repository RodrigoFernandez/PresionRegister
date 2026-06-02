# CONVENTIONS.md

Convenciones de estilo y patrones de código para PresionRegister.

## Lenguaje

- **Mensajes, logs, descripciones de campos y documentación**: español.
- **Identificadores** (variables, funciones, clases, módulos): español o inglés, manteniendo consistencia dentro del mismo archivo.
- **Comentarios en código**: evitar salvo que aporten información no evidente. No comentar lo que el código ya dice.

## Naming

| Elemento | Convención | Ejemplo |
|---|---|---|
| Módulos | `snake_case` | `spreadsheet.py` |
| Paquetes | `snake_case` corto | `presionregister` |
| Funciones | `snake_case` | `iniciar_cliente_google_sheets` |
| Variables | `snake_case` | `web_app_url` |
| Clases | `PascalCase` | `GoogleSheetManager`, `RegistroPresion` |
| Constantes | `UPPER_SNAKE_CASE` | `MAX_PRESSURE` |
| Modelos Pydantic | `PascalCase`, singular o el sufijo semántico (`Registro`, `Respuesta`) | `RegistroPresion`, `RespuestaRegistro` |
| Instancias de logger | `log` (singleton en `logger.py`) | `log.info(...)` |

## Pydantic v2

- Usar `Field(...)` para campos requeridos y `Field(default=...)` para opcionales.
- Incluir `description` en español para los campos expuestos en la API.
- Usar `Field(..., ge=0, le=250)` para rangos numéricos; `Field(..., pattern=...)` para strings con formato.
- `model_config` con `SettingsConfigDict(env_file=".env")` sólo en modelos de configuración.
- No usar `validator`/`root_validator` de v1: usar `field_validator` / `model_validator` de v2.

## Async

- Endpoints de FastAPI siempre `async def`.
- Llamadas a I/O externo (httpx) siempre dentro de `async with httpx.AsyncClient(...) as cliente:`.
- El método que consume el cliente externo es `async def`.

## Manejo de errores

- En endpoints: usar `raise HTTPException(status_code=..., detail=...)`. No retornar tuplas ni `None`.
- Antes de lanzar, loggear con `log.error(...)` o `log.exception(...)` para preservar el contexto.
- En capas internas (`spreadsheet.py`): `raise Exception(...)` con mensaje descriptivo; el endpoint traduce a `HTTPException`.
- No capturar `Exception` de forma silenciosa (sin loggear ni re-lanzar).

## Logger

- Usar **siempre** la instancia global `log` de `src/presionregister.logger`.
- Niveles:
  - `log.info` para operaciones exitosas relevantes.
  - `log.error` para errores recuperables o de configuración.
  - `log.exception` (dentro de un `except`) para errores con stacktrace completo.
- No usar `print(...)` para logging. La única excepción actual (`spreadsheet.py:41`) debe migrarse a `log.error`.

## Imports

- Absolutos desde el paquete: `from src.presionregister.config import settings`.
- Dentro de `src/presionregister/*`, usar imports relativos: `from .models import PresionRegister`.
- Agrupar en orden: stdlib → terceros → locales, separados por línea en blanco.

## Tipado

- Anotaciones de tipo explícitas en funciones públicas (endpoints, métodos de clases exportadas).
- Tipos de Pydantic preferidos sobre `dict`/`Any` para payloads de entrada/salida.
- Para configuración: tipos concretos (`str`, `int`, `bool`), nunca `Any`.

## Estructura de archivos

- Un módulo = una responsabilidad. `config.py` no debe hacer logging; `spreadsheet.py` no debe definir modelos.
- Constantes y configuración al inicio del archivo; funciones y clases debajo.
- Si un archivo supera ~150 líneas, considerar extraer.

## Git

- Mensajes de commit en español, imperativo y breve: `Agregado de validación de rango en RegistroPresion`.
- Un commit por cambio lógico. No mezclar refactors con features.
- No hacer `git push` sin pedido explícito.
