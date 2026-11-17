"""Entidad Alineamiento (componente Ejecución y persistencia, capa de dominio).

Cada alineamiento es un hit que BLAST+ encontró para la query. Es experto en
información de sus porcentajes (regla R1 del diseño detallado).
"""


class Alineamiento:
    """Un hit devuelto por BLAST+, convertido en entidad del dominio."""

    def __init__(self, hit: dict, longitud_query: int) -> None:
        self.hit_id: str = str(hit["hit_id"])
        self.descripcion: str = str(hit.get("descripcion", ""))
        self.score: float = float(hit["score"])
        self.evalue: float = float(hit["evalue"])
        self.identidades: int = int(hit["identidades"])
        self.longitud_alineamiento: int = int(hit["longitud_alineamiento"])
        self.query_desde: int = int(hit["query_desde"])
        self.query_hasta: int = int(hit["query_hasta"])
        self.longitud_query: int = longitud_query

    def porcentaje_identidad(self) -> float:
        """R1: identidades / longitud del alineamiento x 100."""
        return self.identidades / self.longitud_alineamiento * 100

    def porcentaje_cobertura(self) -> float:
        """R1: tramo de la query cubierto / longitud de la query x 100.

        BLAST+ informa las posiciones de la query de forma inclusiva (1..n), por
        eso el tramo cubierto es ``hasta - desde + 1``.
        """
        tramo_cubierto = abs(self.query_hasta - self.query_desde) + 1
        return tramo_cubierto / self.longitud_query * 100
