"""AdaptadorBlastCli · lectura de la salida (EC-02, R5) y ejecución del subproceso (R4).

El subproceso se reemplaza con monkeypatch: la prueba no necesita BLAST+ instalado.
"""

import logging
import subprocess
from pathlib import Path

import pytest

from aplicacion.adaptador_blast import ErrorBlast
from infraestructura.adaptador_blast_cli import AdaptadorBlastCli

DATOS = Path(__file__).parent.parent / "datos"
SALIDA_CONOCIDA = (DATOS / "salida_blastn_2_14.xml").read_text(encoding="utf-8")
SALIDA_CON_CAMPOS_NUEVOS = (DATOS / "salida_blastn_con_campos_nuevos.xml").read_text(encoding="utf-8")


def salida_con_hits(*hits: str) -> str:
    return f"<BlastOutput><BlastOutput_iterations><Iteration><Iteration_hits>{''.join(hits)}" \
           f"</Iteration_hits></Iteration></BlastOutput_iterations></BlastOutput>"


class SubprocesoFalso:
    """Reemplaza a subprocess.run y registra con qué se lo llamó."""

    def __init__(self, codigo=0, stdout=SALIDA_CONOCIDA, stderr="", excepcion=None):
        self.codigo, self.stdout, self.stderr, self.excepcion = codigo, stdout, stderr, excepcion
        self.llamadas = []

    def __call__(self, comando, **opciones):
        self.llamadas.append((comando, opciones))
        if self.excepcion:
            raise self.excepcion
        return subprocess.CompletedProcess(comando, self.codigo, self.stdout, self.stderr)


@pytest.fixture
def subproceso(monkeypatch):
    falso = SubprocesoFalso()
    monkeypatch.setattr(subprocess, "run", falso)
    return falso


# --- leer_salida ----------------------------------------------------------------------

def test_cp22_lee_los_campos_obligatorios_de_cada_hit():
    hits = AdaptadorBlastCli().leer_salida(SALIDA_CONOCIDA)
    assert hits[0] == {"hit_id": "NR_024570.1", "descripcion": "Escherichia coli strain U 5/41 16S ribosomal RNA",
                       "score": "268.5", "evalue": "2.1e-71", "identidades": "144",
                       "longitud_alineamiento": "144", "query_desde": "1", "query_hasta": "144"}
    assert len(hits) == 2


def test_cp23_salida_conocida_no_deja_advertencias(caplog):
    with caplog.at_level(logging.WARNING, logger="localblast.adaptador_blast"):
        AdaptadorBlastCli().leer_salida(SALIDA_CONOCIDA)
    assert caplog.records == []


def test_cp24_ec02_campos_nuevos_no_alteran_los_obligatorios_y_se_advierten(caplog):
    """EC-02: misma salida con campos de una versión nueva -> mismos hits + advertencia."""
    with caplog.at_level(logging.WARNING, logger="localblast.adaptador_blast"):
        hits = AdaptadorBlastCli().leer_salida(SALIDA_CON_CAMPOS_NUEVOS)
    assert hits == AdaptadorBlastCli().leer_salida(SALIDA_CONOCIDA)
    assert len(caplog.records) == 1
    assert "Hit_taxid" in caplog.text and "Hsp_cigar" in caplog.text


def test_cp25_si_falta_un_campo_obligatorio_lanza_error_blast():
    hit = "<Hit><Hit_id>h1</Hit_id><Hit_hsps><Hsp><Hsp_bit-score>10</Hsp_bit-score></Hsp></Hit_hsps></Hit>"
    with pytest.raises(ErrorBlast, match="campos obligatorios"):
        AdaptadorBlastCli().leer_salida(salida_con_hits(hit))


def test_cp26_xml_invalido_lanza_error_blast():
    with pytest.raises(ErrorBlast, match="XML válido"):
        AdaptadorBlastCli().leer_salida("BLAST+ escribió texto, no XML")


def test_cp27_un_hit_sin_hsp_se_ignora():
    assert AdaptadorBlastCli().leer_salida(salida_con_hits("<Hit><Hit_id>h1</Hit_id><Hit_hsps/></Hit>")) == []


def test_cp28_salida_sin_hits_devuelve_lista_vacia():
    assert AdaptadorBlastCli().leer_salida(salida_con_hits()) == []


# --- ejecutar -------------------------------------------------------------------------

def test_cp29_invoca_blast_con_salida_xml_base_y_parametros_y_la_query_por_stdin(subproceso):
    hits = AdaptadorBlastCli().ejecutar("blastn", ">q\nACGT", "base_demo", False, {"evalue": "0.001"})
    comando, opciones = subproceso.llamadas[0]
    assert comando == ["blastn", "-db", "base_demo", "-outfmt", "5", "-evalue", "0.001"]
    assert opciones["input"] == ">q\nACGT"
    assert len(hits) == 2


def test_cp30_en_modo_remoto_agrega_la_flag_remote(subproceso):
    AdaptadorBlastCli().ejecutar("blastp", "MKV", "swissprot", True, {})
    assert "-remote" in subproceso.llamadas[0][0]


def test_cp31_usa_la_carpeta_de_binarios_si_se_configuro(subproceso):
    AdaptadorBlastCli("/opt/blast/bin").ejecutar("blastn", "ACGT", "b", False, {})
    assert Path(subproceso.llamadas[0][0][0]) == Path("/opt/blast/bin/blastn")


def test_cp32_codigo_de_salida_distinto_de_cero_lanza_error_con_el_mensaje_de_blast(subproceso):
    subproceso.codigo, subproceso.stderr = 2, "BLAST Database error: No alias or index file found\n"
    with pytest.raises(ErrorBlast, match="BLAST Database error"):
        AdaptadorBlastCli().ejecutar("blastn", "ACGT", "nt", False, {})


def test_cp33_error_sin_mensaje_informa_el_codigo_de_salida(subproceso):
    subproceso.codigo, subproceso.stderr = 3, ""
    with pytest.raises(ErrorBlast, match="código 3"):
        AdaptadorBlastCli().ejecutar("blastn", "ACGT", "nt", False, {})


def test_cp34_blast_no_instalado_lanza_error_blast(subproceso):
    subproceso.excepcion = FileNotFoundError()
    with pytest.raises(ErrorBlast, match="No se encontró"):
        AdaptadorBlastCli().ejecutar("blastn", "ACGT", "nt", False, {})


def test_cp35_ejecucion_que_supera_el_tiempo_maximo_lanza_error_blast(subproceso):
    subproceso.excepcion = subprocess.TimeoutExpired("blastn", 1)
    with pytest.raises(ErrorBlast, match="tiempo máximo"):
        AdaptadorBlastCli(tiempo_maximo_segundos=1).ejecutar("blastn", "ACGT", "nt", False, {})


def test_cp36_programa_desconocido_se_rechaza_sin_lanzar_subproceso(subproceso):
    with pytest.raises(ErrorBlast, match="Programa"):
        AdaptadorBlastCli().ejecutar("rm", "ACGT", "nt", False, {})
    assert subproceso.llamadas == []


def test_cp37_parametro_no_admitido_se_rechaza_sin_lanzar_subproceso(subproceso):
    with pytest.raises(ErrorBlast, match="Parámetro"):
        AdaptadorBlastCli().ejecutar("blastn", "ACGT", "nt", False, {"out": "/etc/passwd"})
    assert subproceso.llamadas == []
