"""ModeloResultados (Aplicación Web, componente Modelo de resultados, rol Modelo del MVC).

Conserva las filas recibidas para la tabla. En HU11 sumará el filtrado.
"""

from interfaz.cliente.observable import Observable


class ModeloResultados(Observable):
    def __init__(self) -> None:
        super().__init__()
        self._filas_recibidas: list[dict] = []

    def cargar(self, filas: list[dict]) -> None:
        self._filas_recibidas = [dict(fila) for fila in filas]
        self._notificar()

    def filas(self) -> list[dict]:
        return [dict(fila) for fila in self._filas_recibidas]
