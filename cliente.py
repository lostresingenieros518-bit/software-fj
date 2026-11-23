"""Clase Cliente con validaciones y encapsulación de datos personales."""
import re
from entidades import EntidadBase
from excepciones import ClienteInvalidoError
from logger import log


class Cliente(EntidadBase):
    """Cliente de Software FJ. Sus datos son privados y se validan al asignarse."""

    def __init__(self, nombre: str, documento: str, correo: str, telefono: str):
        super().__init__()
        # Los setters (propiedades) validan cada dato; si falla lanzan ClienteInvalidoError
        self.nombre = nombre
        self.documento = documento
        self.correo = correo
        self.telefono = telefono
        log.info(f"Cliente creado: id={self.id} nombre={self._nombre}")

    # ---------- nombre ----------
    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str):
        # Debe ser texto, tener al menos 3 caracteres y solo letras/espacios
        if not isinstance(valor, str) or len(valor.strip()) < 3:
            raise ClienteInvalidoError("El nombre debe tener al menos 3 caracteres")
        if not re.fullmatch(r"[A-Za-zÁÉÍÓÚáéíóúÑñ ]+", valor.strip()):
            raise ClienteInvalidoError("El nombre solo puede contener letras y espacios")
        self._nombre = valor.strip()

    # ---------- documento ----------
    @property
    def documento(self) -> str:
        return self._documento

    @documento.setter
    def documento(self, valor: str):
        # Solo dígitos, entre 6 y 12
        if not isinstance(valor, str) or not re.fullmatch(r"\d{6,12}", valor):
            raise ClienteInvalidoError("El documento debe tener entre 6 y 12 dígitos")
        self._documento = valor

    # ---------- correo ----------
    @property
    def correo(self) -> str:
        return self._correo

    @correo.setter
    def correo(self, valor: str):
        if not isinstance(valor, str) or not re.fullmatch(r"[\w.+-]+@[\w-]+\.[\w.]+", valor):
            raise ClienteInvalidoError("Correo electrónico con formato inválido")
        self._correo = valor.lower()

    # ---------- teléfono ----------
    @property
    def telefono(self) -> str:
        return self._telefono

    @telefono.setter
    def telefono(self, valor: str):
        if not isinstance(valor, str) or not re.fullmatch(r"\d{7,10}", valor):
            raise ClienteInvalidoError("El teléfono debe tener entre 7 y 10 dígitos")
        self._telefono = valor

    def describir(self) -> str:
        # Se oculta parte del documento para proteger datos personales
        oculto = "*" * (len(self._documento) - 3) + self._documento[-3:]
        return f"Cliente #{self.id}: {self._nombre} (doc {oculto}, {self._correo})"
