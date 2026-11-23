"""Clase abstracta Servicio y tres servicios especializados (polimorfismo)."""
from abc import abstractmethod
from entidades import EntidadBase
from excepciones import (ServicioInvalidoError, CalculoInconsistenteError,
                         ParametroFaltanteError)
from logger import log

IVA = 0.19  # impuesto por defecto


class Servicio(EntidadBase):
    """Servicio genérico: define el contrato que deben cumplir todos los servicios."""

    def __init__(self, nombre: str, tarifa_hora: float):
        super().__init__()
        # Validación común a todos los servicios
        if not isinstance(nombre, str) or not nombre.strip():
            raise ServicioInvalidoError("El servicio necesita un nombre")
        if not isinstance(tarifa_hora, (int, float)) or tarifa_hora <= 0:
            raise ServicioInvalidoError("La tarifa por hora debe ser un número positivo")
        self._nombre = nombre.strip()
        self._tarifa_hora = float(tarifa_hora)
        self._disponible = True  # estado de disponibilidad

    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def tarifa_hora(self) -> float:
        return self._tarifa_hora

    @property
    def disponible(self) -> bool:
        return self._disponible

    @disponible.setter
    def disponible(self, valor: bool):
        self._disponible = bool(valor)

    # ---------- métodos abstractos (cada servicio los sobrescribe) ----------
    @abstractmethod
    def validar_parametros(self, horas: float) -> None:
        """Valida que la duración solicitada sea válida para este servicio."""

    @abstractmethod
    def costo_base(self, horas: float) -> float:
        """Costo sin impuestos ni descuentos."""

    # ---------- sobrecarga de métodos (parámetros opcionales) ----------
    def calcular_costo(self, horas: float, impuesto: float = 0.0,
                       descuento: float = 0.0) -> float:
        """Sobrecarga 1: costo simple (horas), 2: con impuesto, 3: con impuesto y descuento."""
        self.validar_parametros(horas)
        if not (0 <= impuesto <= 1) or not (0 <= descuento <= 1):
            raise CalculoInconsistenteError("Impuesto y descuento deben estar entre 0 y 1")
        total = self.costo_base(horas) * (1 + impuesto) * (1 - descuento)
        if total <= 0:
            raise CalculoInconsistenteError("El costo calculado no es válido")
        return round(total, 2)

    def calcular_costo_con_iva(self, horas: float) -> float:
        """Variante: aplica el IVA estándar."""
        return self.calcular_costo(horas, impuesto=IVA)

    def calcular_costo_total(self, horas: float, codigo_descuento: str = None) -> float:
        """Variante: IVA y descuento opcional según un código promocional."""
        descuentos = {"FJ10": 0.10, "FJ20": 0.20}
        if codigo_descuento is None:
            return self.calcular_costo_con_iva(horas)
        if codigo_descuento not in descuentos:
            raise ParametroFaltanteError(f"Código de descuento desconocido: {codigo_descuento}")
        return self.calcular_costo(horas, IVA, descuentos[codigo_descuento])

    def describir(self) -> str:
        estado = "disponible" if self._disponible else "NO disponible"
        return f"{self.__class__.__name__} '{self._nombre}' ${self._tarifa_hora:,.0f}/h ({estado})"


class ReservaSala(Servicio):
    """Servicio de reserva de salas: depende de la capacidad."""

    def __init__(self, nombre: str, tarifa_hora: float, capacidad: int):
        super().__init__(nombre, tarifa_hora)
        if not isinstance(capacidad, int) or capacidad <= 0:
            raise ServicioInvalidoError("La capacidad de la sala debe ser un entero positivo")
        self._capacidad = capacidad

    def validar_parametros(self, horas: float) -> None:
        # Una sala se reserva entre 1 y 12 horas
        if not isinstance(horas, (int, float)) or not 1 <= horas <= 12:
            raise ServicioInvalidoError("Una sala se reserva entre 1 y 12 horas")

    def costo_base(self, horas: float) -> float:
        return self._tarifa_hora * horas

    def describir(self) -> str:
        return super().describir() + f" - capacidad {self._capacidad} personas"


class AlquilerEquipo(Servicio):
    """Alquiler de equipos: cobra un depósito fijo además de las horas."""

    def __init__(self, nombre: str, tarifa_hora: float, deposito: float):
        super().__init__(nombre, tarifa_hora)
        if not isinstance(deposito, (int, float)) or deposito < 0:
            raise ServicioInvalidoError("El depósito no puede ser negativo")
        self._deposito = float(deposito)

    def validar_parametros(self, horas: float) -> None:
        if not isinstance(horas, (int, float)) or not 1 <= horas <= 72:
            raise ServicioInvalidoError("Un equipo se alquila entre 1 y 72 horas")

    def costo_base(self, horas: float) -> float:
        return self._tarifa_hora * horas + self._deposito

    def describir(self) -> str:
        return super().describir() + f" - depósito ${self._deposito:,.0f}"


class Asesoria(Servicio):
    """Asesoría especializada: recargo por nivel del asesor."""

    NIVELES = {"junior": 1.0, "senior": 1.5, "experto": 2.0}

    def __init__(self, nombre: str, tarifa_hora: float, nivel: str):
        super().__init__(nombre, tarifa_hora)
        if nivel not in self.NIVELES:
            raise ServicioInvalidoError(f"Nivel de asesor inválido: {nivel}")
        self._nivel = nivel

    def validar_parametros(self, horas: float) -> None:
        if not isinstance(horas, (int, float)) or not 0.5 <= horas <= 8:
            raise ServicioInvalidoError("Una asesoría dura entre 0.5 y 8 horas")

    def costo_base(self, horas: float) -> float:
        return self._tarifa_hora * horas * self.NIVELES[self._nivel]

    def describir(self) -> str:
        return super().describir() + f" - asesor {self._nivel}"
