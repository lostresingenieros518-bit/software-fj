"""Gestor del sistema: administra listas internas de clientes, servicios y reservas."""
from cliente import Cliente
from servicios import Servicio
from reserva import Reserva
from excepciones import ErrorSoftwareFJ, ParametroFaltanteError
from logger import log


class GestorFJ:
    def __init__(self):
        # Listas internas: no se usa base de datos
        self.clientes: list[Cliente] = []
        self.servicios: list[Servicio] = []
        self.reservas: list[Reserva] = []

    def registrar_cliente(self, **datos) -> Cliente | None:
        """Crea y registra un cliente. Si hay error lo registra y devuelve None."""
        try:
            cliente = Cliente(**datos)
        except TypeError as e:
            # Parámetros faltantes o sobrantes: se convierte en excepción propia
            err = ParametroFaltanteError(f"Datos incompletos para el cliente: {e}")
            log.error(str(err))
            print(f"  [ERROR] {err}")
            return None
        except ErrorSoftwareFJ as e:
            log.error(f"Registro de cliente rechazado: {e}")
            print(f"  [ERROR] {e}")
            return None
        else:
            self.clientes.append(cliente)
            print(f"  [OK] {cliente}")
            return cliente

    def crear_servicio(self, clase, *args, **kwargs) -> Servicio | None:
        """Crea un servicio de la clase indicada (polimorfismo) y lo registra."""
        try:
            servicio = clase(*args, **kwargs)
        except (ErrorSoftwareFJ, TypeError) as e:
            log.error(f"Creación de servicio rechazada: {e}")
            print(f"  [ERROR] {e}")
            return None
        else:
            self.servicios.append(servicio)
            log.info(f"Servicio creado: {servicio.describir()}")
            print(f"  [OK] {servicio.describir()}")
            return servicio

    def crear_reserva(self, cliente, servicio, horas, descuento=None) -> float | None:
        """Crea, confirma y procesa una reserva completa. Devuelve el total o None."""
        try:
            reserva = Reserva(cliente, servicio, horas)
            reserva.confirmar()
            total = reserva.procesar(descuento)
        except ErrorSoftwareFJ as e:
            # Se registra el error junto con su causa original (si existe)
            causa = f" | causa: {e.__cause__}" if e.__cause__ else ""
            log.error(f"Reserva fallida: {e}{causa}")
            print(f"  [ERROR] {e}{causa}")
            return None
        else:
            self.reservas.append(reserva)
            print(f"  [OK] {reserva} -> total ${total:,.2f}")
            return total
