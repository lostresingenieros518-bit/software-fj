"""Simulación de al menos 10 operaciones (válidas e inválidas) de Software FJ."""
from gestor import GestorFJ
from servicios import ReservaSala, AlquilerEquipo, Asesoria
from logger import log


def main():
    log.info("===== INICIO DE LA SIMULACIÓN =====")
    g = GestorFJ()

    print("\n1. Cliente válido")
    ana = g.registrar_cliente(nombre="Ana Pérez", documento="1234567890",
                              correo="ana@mail.com", telefono="3001234567")

    print("\n2. Cliente con correo inválido")
    g.registrar_cliente(nombre="Luis Gómez", documento="9876543", correo="luis-sin-arroba",
                        telefono="3109876543")

    print("\n3. Cliente con parámetros faltantes")
    g.registrar_cliente(nombre="Marta Ruiz", documento="1122334455")

    print("\n4. Cliente válido (segundo)")
    carlos = g.registrar_cliente(nombre="Carlos Díaz", documento="5566778899",
                                 correo="carlos@mail.com", telefono="3205556677")

    print("\n5. Servicio sala válido")
    sala = g.crear_servicio(ReservaSala, "Sala Innovación", 50000, 12)

    print("\n6. Servicio equipo válido")
    equipo = g.crear_servicio(AlquilerEquipo, "Portátil Pro", 8000, 100000)

    print("\n7. Servicio asesoría mal formado (nivel inexistente)")
    g.crear_servicio(Asesoria, "Asesoría Cloud", 70000, "maestro")

    print("\n8. Asesoría válida")
    asesoria = g.crear_servicio(Asesoria, "Asesoría Python", 70000, "senior")

    print("\n9. Reserva exitosa de sala con IVA")
    g.crear_reserva(ana, sala, 3)

    print("\n10. Reserva fallida: duración fuera de rango (cadena de excepciones)")
    g.crear_reserva(ana, sala, 20)

    print("\n11. Reserva exitosa de equipo con descuento FJ10")
    g.crear_reserva(carlos, equipo, 24, "FJ10")

    print("\n12. Reserva fallida: servicio no disponible")
    asesoria.disponible = False
    g.crear_reserva(carlos, asesoria, 2)

    print("\n13. Reserva fallida: cliente inexistente (None)")
    g.crear_reserva(None, sala, 2)

    print("\n14. Reserva con código de descuento inválido")
    g.crear_reserva(ana, equipo, 5, "XX99")

    print("\n15. Reserva válida tras los errores (el sistema sigue activo)")
    asesoria.disponible = True
    g.crear_reserva(carlos, asesoria, 2, "FJ20")

    print(f"\nResumen: {len(g.clientes)} clientes, {len(g.servicios)} servicios, "
          f"{len(g.reservas)} reservas exitosas.")
    log.info("===== FIN DE LA SIMULACIÓN =====")


if __name__ == "__main__":
    main()
