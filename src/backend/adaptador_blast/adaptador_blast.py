"""Interfaz AdaptadorBlast: lo único que el dominio sabe de BLAST+.

ControladorEjecucion depende de esta interfaz y no de una implementación concreta.
Así las pruebas pueden reemplazar al adaptador por un doble, y la aplicación usa
AdaptadorBlastCli (con BLAST+ real o simulado).
"""

from abc import ABC, abstractmethod
from typing import TypedDict


class ErrorBlast(Exception):
    """Error de BLAST+; su mensaje es el que informó BLAST+, sin reinterpretar."""


class Hit(TypedDict):
    """Hit leído de la salida de BLAST+, como datos simples (no como entidad)."""

    id_hit: str
    descripcion: str
    score: float
    evalue: float
    identidades: int
    longitud_alineamiento: int
    query_desde: int
    query_hasta: int


class AdaptadorBlast(ABC):
    """Interfaz para invocar a BLAST+ sin conocer cómo se lo ejecuta ni su formato de salida."""

    @abstractmethod
    def ejecutar(
        self,
        variante: str,
        secuencia: str,
        base_datos: str,
        remota: bool,
        parametros: dict,
    ) -> list[Hit]:
        """Invoca a BLAST+ y devuelve sus hits; lanza ErrorBlast si BLAST+ falla."""
