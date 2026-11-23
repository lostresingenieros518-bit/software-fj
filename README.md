# Software FJ – Sistema Integral de Gestión de Clientes, Servicios y Reservas

Curso Programación (213023) – UNAD – Fase 4. Python 3.10+, sin bases de datos (solo archivo de logs).

## Ejecutar
```
python main.py
```
Genera `software_fj.log` con todos los eventos y errores.

## Estructura
| Archivo | Contenido |
|---|---|
| `excepciones.py` | Excepciones personalizadas (jerarquía desde `ErrorSoftwareFJ`) |
| `logger.py` | Configuración del archivo de logs |
| `entidades.py` | Clase abstracta `EntidadBase` |
| `cliente.py` | `Cliente` con validaciones y encapsulación |
| `servicios.py` | `Servicio` (abstracta), `ReservaSala`, `AlquilerEquipo`, `Asesoria`; costos sobrecargados |
| `reserva.py` | `Reserva`: confirmar, cancelar, procesar (try/except/else/finally, encadenamiento) |
| `gestor.py` | `GestorFJ`: listas internas y operaciones controladas |
| `main.py` | 15 simulaciones válidas e inválidas |

## Conceptos aplicados
Abstracción, herencia, polimorfismo, encapsulación, sobrecarga (parámetros opcionales), `try/except`, `try/except/else`, `finally`, `raise ... from e`, logging.
