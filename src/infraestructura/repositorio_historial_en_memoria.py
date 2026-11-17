"""RepositorioHistorialEnMemoria (componente Acceso a datos, capa de datos).

Guarda el historial en una lista de Python. Sirve para las pruebas y para correr
el sistema sin instalar nada (decisión D9). Usa un candado porque el servidor
atiende cada solicitud en su propio hilo (EC-01).
"""

import threading

from aplicacion.repositorio_historial import RepositorioHistorial
from dominio.busqueda import Busqueda


class RepositorioHistorialEnMemoria(RepositorioHistorial):
    def __init__(self) -> None:
        self._busquedas: list[Busqueda] = []
        self._candado = threading.Lock()

    def guardar(self, busqueda: Busqueda) -> None:
        with self._candado:
            self._busquedas.append(busqueda)

    @property
    def busquedas(self) -> tuple[Busqueda, ...]:
        """Búsquedas guardadas, en orden (solo lectura)."""
        with self._candado:
            return tuple(self._busquedas)
