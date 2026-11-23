"""Configuración del archivo de logs (únicos archivos permitidos por el enunciado)."""
import logging

# Nombre del archivo donde se guardan eventos y errores
ARCHIVO_LOG = "software_fj.log"


def obtener_logger() -> logging.Logger:
    """Crea (una sola vez) y devuelve el logger del sistema."""
    logger = logging.getLogger("software_fj")
    # Si ya tiene manejadores, se reutiliza para no duplicar líneas
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        manejador = logging.FileHandler(ARCHIVO_LOG, encoding="utf-8")
        formato = logging.Formatter("%(asctime)s | %(levelname)-8s | %(message)s")
        manejador.setFormatter(formato)
        logger.addHandler(manejador)
    return logger


# Logger compartido por todos los módulos
log = obtener_logger()
