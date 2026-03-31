# Configuración del logger
import logging
import sys

# Configuración básica del logger
def setup_logging():
    logger = logging.getLogger("presion_register")
    logger.setLevel(logging.INFO)

    # Formato del mensaje
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # Handler para la consola
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    
    if not logger.handlers:
        logger.addHandler(console_handler)
    
    return logger

# Instancia global
log = setup_logging()
    