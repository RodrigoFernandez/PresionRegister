FROM python:3.12-slim

# Instalar uv directamente
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app
COPY . .

# Sincronizar dependencias
RUN uv sync --frozen

# Ejecutar con el mínimo de recursos
CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]
