"""ModeloBusqueda (Aplicación Web, componente Modelo de búsqueda, rol Modelo del MVC).

Conserva la configuración validada y el estado de la ejecución (regla R6).
"""

from interfaz.cliente.observable import Observable

LISTA = "lista"
EN_EJECUCION = "en_ejecucion"
FINALIZADA = "finalizada"
CON_ERROR = "con_error"


class ModeloBusqueda(Observable):
    def __init__(self) -> None:
        super().__init__()
        self._configuracion_validada: dict = {}
        self._estado: str = LISTA
        self._error: str | None = None

    def establecer_configuracion(self, configuracion: dict) -> None:
        """Lo deja hecho la validación (HU03 a HU07), precondición de esta HU."""
        self._configuracion_validada = dict(configuracion)
        self._estado = LISTA
        self._error = None
        self._notificar()

    def configuracion(self) -> dict:
        return dict(self._configuracion_validada)

    def estado(self) -> str:
        return self._estado

    def marcar_en_ejecucion(self) -> None:
        self._estado = EN_EJECUCION
        self._error = None
        self._notificar()

    def marcar_finalizada(self) -> None:
        self._estado = FINALIZADA
        self._notificar()

    def registrar_error(self, mensaje: str) -> None:
        self._estado = CON_ERROR
        self._error = mensaje
        self._notificar()

    def mensaje_error(self) -> str | None:
        return self._error
