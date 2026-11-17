"""ControladorEjecucion (componente Ejecución y persistencia, capa de dominio).

Sigue la secuencia 1 del diseño detallado, mensaje por mensaje. No tiene ningún
``if`` sobre reglas del negocio: si BLAST+ falla, ErrorBlast corta el flujo antes
de registrar y de guardar (R4), y el orden guardar -> tabla_resultados cumple R3.
"""

from collections.abc import Callable
from datetime import datetime

from aplicacion.adaptador_blast import AdaptadorBlast
from aplicacion.repositorio_historial import RepositorioHistorial
from dominio.busqueda import Busqueda


class ControladorEjecucion:
    """Orquesta la ejecución de una búsqueda validada en el servidor."""

    def __init__(
        self,
        adaptador_blast: AdaptadorBlast,
        historial: RepositorioHistorial,
        reloj: Callable[[], datetime] = datetime.now,
    ) -> None:
        self._adaptador_blast = adaptador_blast
        self._historial = historial
        self._reloj = reloj

    def ejecutar_busqueda(self, configuracion: dict) -> list[dict]:
        busqueda = Busqueda(configuracion, self._reloj())
        hits = self._adaptador_blast.ejecutar(
            busqueda.programa,
            busqueda.secuencia,
            busqueda.base_datos,
            busqueda.remota,
            busqueda.parametros,
        )
        busqueda.registrar_resultados(hits)
        self._historial.guardar(busqueda)
        return busqueda.tabla_resultados()
