"""Clase abstracta general que representa las entidades del sistema."""
from abc import ABC, abstractmethod


class EntidadBase(ABC):
    """Toda entidad (cliente, servicio, reserva) tiene un id y se puede describir."""

    _contador = 0  # contador de clase para generar ids únicos

    def __init__(self):
        EntidadBase._contador += 1            # incrementa el contador global
        self._id = EntidadBase._contador      # id encapsulado (solo lectura)

    @property
    def id(self) -> int:
        """Identificador único de la entidad."""
        return self._id

    @abstractmethod
    def describir(self) -> str:
        """Cada entidad debe devolver una descripción en texto."""

    def __str__(self) -> str:
        return self.describir()
