"""ControladorEjecucion: coordina la ejecución de una búsqueda en el servidor.

Sigue la Secuencia 1 del diseño detallado (camino principal). El camino de error
(Secuencia 2) no necesita ningún `if`: si BLAST+ falla, AdaptadorBlast lanza
ErrorBlast y el flujo se corta antes de registrar resultados y de guardar (R4).
El orden "primero se guarda, después se devuelve la tabla" es la regla R3.
"""

from collections.abc import Callable
from datetime import datetime

from backend.acceso_datos.repositorio_historial import RepositorioHistorial
from backend.adaptador_blast.adaptador_blast import AdaptadorBlast, ErrorBlast
from backend.ejecucion.busqueda import Busqueda

__all__ = ["ControladorEjecucion", "ErrorBlast"]


def obtener_hora_actual() -> datetime:
    """Devuelve la fecha y hora actuales con la zona horaria del servidor."""
    return datetime.now().astimezone()


class ControladorEjecucion:
    """Controlador que orquesta la ejecución de una búsqueda sin hacer el trabajo del dominio."""

    def __init__(
        self,
        adaptador: AdaptadorBlast,
        repositorio: RepositorioHistorial,
        reloj: Callable[[], datetime] = obtener_hora_actual,
    ) -> None:
        """Recibe sus colaboradores (adaptador, repositorio y reloj) por inyección."""
        self._adaptador: AdaptadorBlast = adaptador
        self._repositorio: RepositorioHistorial = repositorio
        self._reloj: Callable[[], datetime] = reloj

    def ejecutar_busqueda(self, configuracion: dict) -> list[dict]:
        """Ejecuta la búsqueda, la guarda en el historial y devuelve las filas de la tabla.

        Lanza ErrorBlast si BLAST+ no termina bien; en ese caso no se guarda nada.
        """
        busqueda = Busqueda(configuracion, self._reloj())
        hits = self._adaptador.ejecutar(
            busqueda.variante,
            busqueda.secuencia,
            busqueda.base_datos,
            busqueda.es_remota,
            busqueda.parametros,
        )
        busqueda.registrar_resultados(hits)
        self._repositorio.guardar(busqueda)
        return busqueda.armar_tabla_resultados()
