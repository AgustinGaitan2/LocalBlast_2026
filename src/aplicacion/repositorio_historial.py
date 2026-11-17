"""Puerto hacia el historial D2 (interfaz que ofrece el componente Acceso a datos).

Polimorfismo y Variaciones protegidas (decisión D9): el controlador llama a
``guardar`` sin saber si el historial está en memoria, en SQLite o en PostgreSQL.
"""

from abc import ABC, abstractmethod

from dominio.busqueda import Busqueda


class RepositorioHistorial(ABC):
    """Guarda una búsqueda terminada con todos sus alineamientos crudos."""

    @abstractmethod
    def guardar(self, busqueda: Busqueda) -> None:
        """Persiste la búsqueda; si falla, lanza una excepción."""
