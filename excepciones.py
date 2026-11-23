"""Excepciones personalizadas del sistema Software FJ."""


class ErrorSoftwareFJ(Exception):
    """Excepción base: todas las excepciones del sistema heredan de esta."""


class ClienteInvalidoError(ErrorSoftwareFJ):
    """Se lanza cuando los datos de un cliente no cumplen las validaciones."""


class ServicioInvalidoError(ErrorSoftwareFJ):
    """Se lanza cuando un servicio se crea con parámetros mal formados."""


class ServicioNoDisponibleError(ErrorSoftwareFJ):
    """Se lanza cuando se intenta reservar un servicio no disponible."""


class ParametroFaltanteError(ErrorSoftwareFJ):
    """Se lanza cuando falta un parámetro obligatorio en una operación."""


class OperacionNoPermitidaError(ErrorSoftwareFJ):
    """Se lanza cuando se intenta una operación que el estado actual no permite."""


class ReservaError(ErrorSoftwareFJ):
    """Error general al crear o procesar una reserva."""


class CalculoInconsistenteError(ErrorSoftwareFJ):
    """Se lanza cuando un cálculo de costos produce un resultado inválido."""
