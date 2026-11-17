"""ControladorBusqueda (Aplicación Web, componente Controlador de búsqueda, rol Controlador del MVC).

Interpreta la acción "ejecutar": toma la configuración del Modelo, cambia el
estado, pide la ejecución al Backend sin bloquear la interfaz (CA-01, decisión D2)
y carga el resultado o el error en los Modelos.
"""

import threading
from collections.abc import Callable

from interfaz.cliente.cliente_backend import ClienteBackend, ErrorEjecucion
from interfaz.cliente.modelo_busqueda import ModeloBusqueda
from interfaz.cliente.modelo_resultados import ModeloResultados


def lanzar_en_hilo(tarea: Callable[[], None]) -> None:
    """Ejecuta la tarea en segundo plano: quien la lanza no queda esperando."""
    threading.Thread(target=tarea, daemon=True).start()


class ControladorBusqueda:
    def __init__(
        self,
        modelo_busqueda: ModeloBusqueda,
        modelo_resultados: ModeloResultados,
        cliente: ClienteBackend,
        lanzar: Callable[[Callable[[], None]], None] = lanzar_en_hilo,
    ) -> None:
        self._modelo_busqueda = modelo_busqueda
        self._modelo_resultados = modelo_resultados
        self._cliente = cliente
        self._lanzar = lanzar

    def preparar(self, configuracion: dict) -> None:
        """Deja la configuración en el Modelo (sustituye a HU03-HU07, fuera de alcance)."""
        self._modelo_busqueda.establecer_configuracion(configuracion)

    def ejecutar(self) -> None:
        configuracion = self._modelo_busqueda.configuracion()
        self._modelo_busqueda.marcar_en_ejecucion()
        self._lanzar(lambda: self._esperar_resultados(configuracion))

    def _esperar_resultados(self, configuracion: dict) -> None:
        try:
            filas = self._cliente.ejecutar_busqueda(configuracion)
        except ErrorEjecucion as error:
            self._modelo_busqueda.registrar_error(error.mensaje)
            return
        self._modelo_resultados.cargar(filas)
        self._modelo_busqueda.marcar_finalizada()
