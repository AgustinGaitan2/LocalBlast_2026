"""Datos y dobles de prueba compartidos por las pruebas del Backend.

Ninguna prueba usa la red, el reloj real ni BLAST+ real (salvo las marcadas `blast_real`):
- `armar_salida_xml` arma salidas de BLAST+ (-outfmt 5) con los hits que cada prueba necesita.
- `AdaptadorDoble` reemplaza a AdaptadorBlast: devuelve hits fijos o lanza ErrorBlast.
- `RepositorioHistorialEnMemoria` (del propio sistema) reemplaza a la base de datos.
"""

from datetime import datetime, timezone

import pytest

from backend.acceso_datos.repositorio_historial_memoria import RepositorioHistorialEnMemoria
from backend.adaptador_blast.adaptador_blast import AdaptadorBlast, ErrorBlast, Hit
from backend.ejecucion.controlador_ejecucion import ControladorEjecucion

FECHA_FIJA = datetime(2026, 11, 21, 15, 30, tzinfo=timezone.utc)

QUERY_420 = ">proteina_demo Proteina de prueba\n" + "\n".join(["A" * 60] * 7) + "\n"


def crear_hit(**cambios) -> Hit:
    """Hit válido de 420 residuos alineados sobre una query de 420; se cambian los campos pedidos."""
    hit = Hit(
        id_hit="demo_var01",
        descripcion="Variante de prueba",
        score=887.1,
        evalue=0.0,
        identidades=419,
        longitud_alineamiento=420,
        query_desde=1,
        query_hasta=420,
    )
    hit.update(cambios)
    return hit


def armar_salida_xml(*hits: dict, campos_extra_hsp: str = "", campos_extra_hit: str = "") -> str:
    """Salida XML de BLAST+ con un <Hit> por cada diccionario recibido."""
    bloques = []
    for numero, hit in enumerate(hits, start=1):
        bloques.append(f"""
        <Hit>
          <Hit_num>{numero}</Hit_num>
          <Hit_id>{hit.get("id", f"hit{numero}")}</Hit_id>
          <Hit_def>{hit.get("def", "Descripcion de prueba")}</Hit_def>
          <Hit_accession>{hit.get("id", f"hit{numero}")}</Hit_accession>
          <Hit_len>{hit.get("len", 420)}</Hit_len>{campos_extra_hit}
          <Hit_hsps>
            <Hsp>
              <Hsp_num>1</Hsp_num>
              <Hsp_bit-score>{hit.get("bits", 100.5)}</Hsp_bit-score>
              <Hsp_score>250</Hsp_score>
              <Hsp_evalue>{hit.get("evalue", 1e-20)}</Hsp_evalue>
              <Hsp_query-from>{hit.get("desde", 1)}</Hsp_query-from>
              <Hsp_query-to>{hit.get("hasta", 420)}</Hsp_query-to>
              <Hsp_hit-from>1</Hsp_hit-from>
              <Hsp_hit-to>420</Hsp_hit-to>
              <Hsp_query-frame>0</Hsp_query-frame>
              <Hsp_hit-frame>0</Hsp_hit-frame>
              <Hsp_identity>{hit.get("ident", 400)}</Hsp_identity>
              <Hsp_positive>410</Hsp_positive>
              <Hsp_gaps>0</Hsp_gaps>
              <Hsp_align-len>{hit.get("largo", 420)}</Hsp_align-len>{campos_extra_hsp}
              <Hsp_qseq>AAAA</Hsp_qseq>
              <Hsp_hseq>AAAA</Hsp_hseq>
              <Hsp_midline>AAAA</Hsp_midline>
            </Hsp>
          </Hit_hsps>
        </Hit>""")
    return f"""<?xml version="1.0"?>
<!DOCTYPE BlastOutput PUBLIC "-//NCBI//NCBI BlastOutput/EN" "http://www.ncbi.nlm.nih.gov/dtd/NCBI_BlastOutput.dtd">
<BlastOutput>
  <BlastOutput_program>blastp</BlastOutput_program>
  <BlastOutput_version>BLASTP 2.12.0+</BlastOutput_version>
  <BlastOutput_iterations>
    <Iteration>
      <Iteration_iter-num>1</Iteration_iter-num>
      <Iteration_hits>{"".join(bloques)}
      </Iteration_hits>
    </Iteration>
  </BlastOutput_iterations>
</BlastOutput>
"""


class AdaptadorDoble(AdaptadorBlast):
    """Doble de AdaptadorBlast: registra con qué se lo llamó y devuelve hits fijos o falla."""

    def __init__(self, hits: list[Hit] | None = None, error: str | None = None) -> None:
        """Configura los hits que devolverá o el error que lanzará."""
        self.hits = hits if hits is not None else [crear_hit()]
        self.error = error
        self.llamadas: list[tuple] = []

    def ejecutar(self, variante, secuencia, base_datos, remota, parametros):
        """Registra la llamada y devuelve los hits configurados, o lanza ErrorBlast."""
        self.llamadas.append((variante, secuencia, base_datos, remota, parametros))
        if self.error is not None:
            raise ErrorBlast(self.error)
        return self.hits


@pytest.fixture
def configuracion() -> dict:
    """Configuración validada de una búsqueda local con blastp."""
    return {
        "secuencia": QUERY_420,
        "variante": "blastp",
        "modo": "local",
        "base_datos": "datos/blastdb/proteinas_demo",
        "parametros": {"evalue": 10, "matrix": "BLOSUM62"},
    }


@pytest.fixture
def repositorio() -> RepositorioHistorialEnMemoria:
    """Historial en memoria, vacío, para inspeccionar lo que se guardó."""
    return RepositorioHistorialEnMemoria()


@pytest.fixture
def armar_controlador(repositorio):
    """Arma un ControladorEjecucion con un adaptador doble, el repositorio en memoria y reloj fijo."""

    def armar(adaptador: AdaptadorBlast) -> ControladorEjecucion:
        """Crea el controlador con el adaptador indicado."""
        return ControladorEjecucion(adaptador, repositorio, reloj=lambda: FECHA_FIJA)

    return armar
