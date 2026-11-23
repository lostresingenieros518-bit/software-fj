"""Clase Reserva: integra cliente, servicio, duración y estado."""
from entidades import EntidadBase
from cliente import Cliente
from servicios import Servicio
from excepciones import (ReservaError, ServicioNoDisponibleError,
                         OperacionNoPermitidaError, ErrorSoftwareFJ)
from logger import log


class Reserva(EntidadBase):
    ESTADOS = ("PENDIENTE", "CONFIRMADA", "CANCELADA", "PROCESADA")

    def __init__(self, cliente: Cliente, servicio: Servicio, horas: float):
        super().__init__()
        # Validaciones de integración
        if not isinstance(cliente, Cliente):
            raise ReservaError("La reserva requiere un cliente válido")
        if not isinstance(servicio, Servicio):
            raise ReservaError("La reserva requiere un servicio válido")
        if not servicio.disponible:
            raise ServicioNoDisponibleError(f"'{servicio.nombre}' no está disponible")
        try:
            # Se valida la duración con el polimorfismo del servicio
            servicio.validar_parametros(horas)
        except ErrorSoftwareFJ as e:
            # Encadenamiento de excepciones: conserva la causa original
            raise ReservaError("Duración inválida para la reserva") from e
        self._cliente = cliente
        self._servicio = servicio
        self._horas = horas
        self._estado = "PENDIENTE"

    @property
    def estado(self) -> str:
        return self._estado

    @property
    def cliente(self) -> Cliente:
        return self._cliente

    def confirmar(self) -> None:
        if self._estado != "PENDIENTE":
            raise OperacionNoPermitidaError(f"No se puede confirmar una reserva {self._estado}")
        self._estado = "CONFIRMADA"
        log.info(f"Reserva {self.id} confirmada")

    def cancelar(self) -> None:
        if self._estado in ("CANCELADA", "PROCESADA"):
            raise OperacionNoPermitidaError(f"No se puede cancelar una reserva {self._estado}")
        self._estado = "CANCELADA"
        log.info(f"Reserva {self.id} cancelada")

    def procesar(self, codigo_descuento: str = None) -> float:
        """Procesa la reserva y devuelve el costo total. Usa try/except/else/finally."""
        total = None
        try:
            if self._estado != "CONFIRMADA":
                raise OperacionNoPermitidaError("Solo se procesan reservas CONFIRMADAS")
            total = self._servicio.calcular_costo_total(self._horas, codigo_descuento)
        except ErrorSoftwareFJ as e:
            log.error(f"Fallo al procesar reserva {self.id}: {e}")
            raise ReservaError(f"No se pudo procesar la reserva {self.id}") from e
        else:
            # Solo se ejecuta si no hubo excepción
            self._estado = "PROCESADA"
            log.info(f"Reserva {self.id} procesada. Total ${total:,.2f}")
            return total
        finally:
            # Siempre se ejecuta, haya error o no
            log.info(f"Intento de procesamiento de reserva {self.id} finalizado")

    def describir(self) -> str:
        return (f"Reserva #{self.id} [{self._estado}] {self._cliente.nombre} -> "
                f"{self._servicio.nombre} ({self._horas} h)")
