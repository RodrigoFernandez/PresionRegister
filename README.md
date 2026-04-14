# PresionRegister

## Para usar esta aplicación
 * para bajar las bibliotecas y la versión de python usada:
  ```
  uv sync
  ```
 * agregar .env con el siguiente contenido:
  ```
  app_web_gs_presion="...
  ```
 * levantar la aplicación con el comando:
  ```
  uv run unicorn main:app --reload
  ```
