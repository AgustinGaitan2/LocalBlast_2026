"""Entidad Busqueda (componente Ejecución y persistencia, capa de dominio).

Raíz del agregado Busqueda-Alineamiento. Guarda la configuración validada y el
momento de ejecución, crea un Alineamiento por cada hit (regla R2: el conjunto
completo, sin filtrar) y arma las filas de la tabla de resultados.
"""

from datetime import datetime

from dominio.alineamiento import Alineamiento


class Busqueda:
    """Búsqueda BLAST ya validada que se ejecuta y queda en el historial."""

    def __init__(self, configuracion: dict, fecha: datetime) -> None:
        self.secuencia: str = configuracion["secuencia"]
        self.programa: str = configuracion["programa"]
        self.base_datos: str = configuracion["base_datos"]
        self.remota: bool = bool(configuracion.get("remota", False))
        self.parametros: dict = dict(configuracion.get("parametros") or {})
        self.fecha: datetime = fecha
        self.alineamientos: list[Alineamiento] = []
        if self.longitud_query() == 0:
            raise ValueError("La secuencia query no tiene residuos.")

    def longitud_query(self) -> int:
        """Cantidad de residuos de la query, sin la línea de encabezado FASTA."""
        lineas = self.secuencia.strip().splitlines()
        residuos = "".join(linea for linea in lineas if not linea.startswith(">"))
        return len("".join(residuos.split()))

    def registrar_resultados(self, hits: list[dict]) -> None:
        """R2: crea un Alineamiento por cada hit, sin descartar ninguno."""
        longitud = self.longitud_query()
        for hit in hits:
            self.alineamientos.append(Alineamiento(hit, longitud))

    def tabla_resultados(self) -> list[dict]:
        """Filas de la tabla de CA-02, una por alineamiento."""
        filas = []
        for alineamiento in self.alineamientos:
            filas.append(
                {
                    "hit_id": alineamiento.hit_id,
                    "descripcion": alineamiento.descripcion,
                    "score": alineamiento.score,
                    "evalue": alineamiento.evalue,
                    "porcentaje_identidad": round(alineamiento.porcentaje_identidad(), 2),
                    "porcentaje_cobertura": round(alineamiento.porcentaje_cobertura(), 2),
                }
            )
        return filas
