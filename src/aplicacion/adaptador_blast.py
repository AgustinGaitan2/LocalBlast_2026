"""Puerto hacia BLAST+ (interfaz que ofrece el componente Adaptador BLAST+).

El controlador depende de esta interfaz y no de sus implementaciones
(AdaptadorBlastCli o AdaptadorBlastSimulado), que viven en infraestructura.
"""

from abc import ABC, abstractmethod


class ErrorBlast(Exception):
    """BLAST+ no terminó bien (regla R4). Corta el flujo antes de guardar."""

    def __init__(self, mensaje: str) -> None:
        super().__init__(mensaje)
        self.mensaje = mensaje


class AdaptadorBlast(ABC):
    """Ejecuta una búsqueda en BLAST+ y devuelve los hits como datos simples (D5)."""

    @abstractmethod
    def ejecutar(
        self,
        programa: str,
        secuencia: str,
        base_datos: str,
        remota: bool,
        parametros: dict,
    ) -> list[dict]:
        """Devuelve un diccionario por hit o lanza ErrorBlast."""
