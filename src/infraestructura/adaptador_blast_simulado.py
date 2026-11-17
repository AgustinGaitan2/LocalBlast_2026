"""AdaptadorBlastSimulado (componente Adaptador BLAST+, capa de datos).

Doble de BLAST+ detrás de la interfaz AdaptadorBlast (decisión D6). Sirve para:

- probar EC-01 con demoras controladas y distintas por búsqueda;
- correr y demostrar el sistema en una máquina sin BLAST+ instalado.

Se comporta como BLAST+ en lo que importa al diseño: devuelve hits como datos
simples y, si la base de datos no existe, termina con error (ErrorBlast).
"""

import time

from aplicacion.adaptador_blast import AdaptadorBlast, ErrorBlast


class AdaptadorBlastSimulado(AdaptadorBlast):
    """Devuelve hits preparados de antemano para cada secuencia, con una demora opcional.

    Los hits se buscan por la secuencia sin espacios al principio ni al final.
    """

    def __init__(
        self,
        hits_preparados: dict[str, list[dict]],
        bases_disponibles: set[str],
        demora_segundos: float | dict[str, float] = 0.0,
        hits_por_defecto: list[dict] | None = None,
    ) -> None:
        self.hits_preparados = hits_preparados
        self.bases_disponibles = bases_disponibles
        self.demora_segundos = demora_segundos
        self.hits_por_defecto = hits_por_defecto or []
        self.invocaciones: list[dict] = []

    def ejecutar(
        self,
        programa: str,
        secuencia: str,
        base_datos: str,
        remota: bool,
        parametros: dict,
    ) -> list[dict]:
        self.invocaciones.append(
            {"programa": programa, "secuencia": secuencia, "base_datos": base_datos,
             "remota": remota, "parametros": parametros}
        )
        time.sleep(self._demora_para(secuencia))
        if base_datos not in self.bases_disponibles:
            raise ErrorBlast(f"BLAST Database error: No alias or index file found for database [{base_datos}].")
        hits = self.hits_preparados.get(secuencia.strip(), self.hits_por_defecto)
        return [dict(hit) for hit in hits]

    def _demora_para(self, secuencia: str) -> float:
        if isinstance(self.demora_segundos, dict):
            return self.demora_segundos.get(secuencia, 0.0)
        return self.demora_segundos
