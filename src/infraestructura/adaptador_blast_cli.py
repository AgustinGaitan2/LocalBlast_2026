"""AdaptadorBlastCli (componente Adaptador BLAST+, capa de datos).

Patrón Adapter: traduce "ejecutá esto y devolveme los hits" a una invocación de
BLAST+ por línea de comandos con salida XML (``-outfmt 5``, decisión D7).

- EC-01 (concurrencia): cada llamada a ``ejecutar`` lanza su propio subproceso y
  espera su salida en el mismo hilo; no hay estado compartido entre búsquedas.
- EC-02 (cambio de versión): ``leer_salida`` toma los campos por su nombre e
  ignora los que no conoce, dejando una advertencia en el log (regla R5).
"""

import logging
import subprocess
from pathlib import Path
from xml.etree import ElementTree

from aplicacion.adaptador_blast import AdaptadorBlast, ErrorBlast

logger = logging.getLogger("localblast.adaptador_blast")

PROGRAMAS = {"blastn", "blastp", "blastx", "tblastn", "tblastx"}
# Parámetros pre-búsqueda que se traducen a flags de BLAST+ (RF de configuración).
PARAMETROS = {"evalue", "word_size", "matrix", "gapopen", "gapextend", "max_target_seqs"}

# Campos que este adaptador conoce de la salida XML de BLAST+ 2.14.
CAMPOS_HIT = {"Hit_num", "Hit_id", "Hit_def", "Hit_accession", "Hit_len", "Hit_hsps"}
CAMPOS_HSP = {
    "Hsp_num", "Hsp_bit-score", "Hsp_score", "Hsp_evalue", "Hsp_query-from",
    "Hsp_query-to", "Hsp_hit-from", "Hsp_hit-to", "Hsp_pattern-from",
    "Hsp_pattern-to", "Hsp_query-frame", "Hsp_hit-frame", "Hsp_identity",
    "Hsp_positive", "Hsp_gaps", "Hsp_align-len", "Hsp_density", "Hsp_qseq",
    "Hsp_hseq", "Hsp_midline",
}
# Campo XML obligatorio -> clave del hit que entiende el dominio.
OBLIGATORIOS_HSP = {
    "Hsp_bit-score": "score",
    "Hsp_evalue": "evalue",
    "Hsp_identity": "identidades",
    "Hsp_align-len": "longitud_alineamiento",
    "Hsp_query-from": "query_desde",
    "Hsp_query-to": "query_hasta",
}


class AdaptadorBlastCli(AdaptadorBlast):
    """Invoca los binarios de BLAST+ como subproceso (DA-03, DA-04)."""

    def __init__(self, directorio_binarios: str = "", tiempo_maximo_segundos: float = 3600) -> None:
        self.directorio_binarios = directorio_binarios
        self.tiempo_maximo_segundos = tiempo_maximo_segundos

    def ejecutar(
        self,
        programa: str,
        secuencia: str,
        base_datos: str,
        remota: bool,
        parametros: dict,
    ) -> list[dict]:
        comando = self._armar_comando(programa, base_datos, remota, parametros)
        try:
            proceso = subprocess.run(
                comando,
                input=secuencia,
                capture_output=True,
                text=True,
                timeout=self.tiempo_maximo_segundos,
            )
        except FileNotFoundError as error:
            raise ErrorBlast(f"No se encontró el programa de BLAST+ '{comando[0]}'.") from error
        except subprocess.TimeoutExpired as error:
            raise ErrorBlast("BLAST+ superó el tiempo máximo de ejecución.") from error
        if proceso.returncode != 0:
            raise ErrorBlast(proceso.stderr.strip() or f"BLAST+ terminó con código {proceso.returncode}.")
        return self.leer_salida(proceso.stdout)

    def leer_salida(self, salida_xml: str) -> list[dict]:
        """Convierte la salida XML en una lista de hits (uno por Hit, con su mejor HSP)."""
        try:
            raiz = ElementTree.fromstring(salida_xml)
        except ElementTree.ParseError as error:
            raise ErrorBlast("La salida de BLAST+ no es un XML válido.") from error
        hits = []
        desconocidos: set[str] = set()
        for hit in raiz.iter("Hit"):
            hsp = hit.find("Hit_hsps/Hsp")
            if hsp is None:
                continue
            desconocidos |= {campo.tag for campo in hit} - CAMPOS_HIT
            desconocidos |= {campo.tag for campo in hsp} - CAMPOS_HSP
            hits.append(self._leer_hit(hit, hsp))
        if desconocidos:
            self.registrar_advertencia(sorted(desconocidos))
        return hits

    def _leer_hit(self, hit: ElementTree.Element, hsp: ElementTree.Element) -> dict:
        datos = {
            "hit_id": hit.findtext("Hit_id"),
            "descripcion": hit.findtext("Hit_def", default=""),
        }
        for campo_xml, clave in OBLIGATORIOS_HSP.items():
            datos[clave] = hsp.findtext(campo_xml)
        faltantes = [clave for clave, valor in datos.items() if valor is None]
        if faltantes:
            raise ErrorBlast(f"La salida de BLAST+ no trae los campos obligatorios: {', '.join(faltantes)}.")
        return datos

    def registrar_advertencia(self, campos: list[str]) -> None:
        logger.warning("La salida de BLAST+ trae campos desconocidos que se ignoran: %s", ", ".join(campos))

    def _armar_comando(self, programa: str, base_datos: str, remota: bool, parametros: dict) -> list[str]:
        if programa not in PROGRAMAS:
            raise ErrorBlast(f"Programa de BLAST+ desconocido: '{programa}'.")
        ejecutable = str(Path(self.directorio_binarios) / programa) if self.directorio_binarios else programa
        comando = [ejecutable, "-db", base_datos, "-outfmt", "5"]
        if remota:
            comando.append("-remote")
        for nombre, valor in parametros.items():
            if nombre not in PARAMETROS:
                raise ErrorBlast(f"Parámetro de BLAST+ no admitido: '{nombre}'.")
            comando += [f"-{nombre}", str(valor)]
        return comando
