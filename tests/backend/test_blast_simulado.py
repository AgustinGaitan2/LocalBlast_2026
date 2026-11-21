"""BLAST+ simulado y ejecución real de subprocesos (reemplazos del sistema externo BLAST+)."""

import sys

import pytest

from backend.adaptador_blast.adaptador_blast_cli import AdaptadorBlastCli, ejecutar_subproceso
from backend.adaptador_blast.blast_simulado import BlastSimulado


def armar_comando(base, *extra):
    """Arma un comando de blastp contra la base indicada, con opciones extra."""
    return ["blastp", "-db", base, "-outfmt", "5", *extra]


def test_el_simulado_devuelve_la_salida_grabada_de_la_base_de_demostracion():
    """CP-38 · Caja blanca, BlastSimulado.__call__ rama "base local conocida"."""
    resultado = BlastSimulado(demora_segundos=0)(armar_comando("datos/blastdb/proteinas_demo"), ">q\nM", None, None)

    assert resultado.codigo == 0
    hits = AdaptadorBlastCli().leer_salida(resultado.salida)
    assert len(hits) == 15 and hits[0]["id_hit"] == "demo_var01"


@pytest.mark.parametrize("directorio", ["/repo", None])
def test_el_simulado_responde_como_blast_si_la_base_local_no_existe(directorio):
    """CP-39 · Caja blanca, rama "base local desconocida" (con y sin carpeta de trabajo): responde
    como BLAST+.
    """
    resultado = BlastSimulado(demora_segundos=0)(armar_comando("datos/blastdb/otra"), ">q\nM", directorio, None)

    assert resultado.codigo == 2
    assert resultado.errores.startswith("BLAST Database error: No alias or index file found")
    assert "[datos/blastdb/otra]" in resultado.errores


def test_el_simulado_acepta_cualquier_base_en_modo_remoto():
    """CP-40 · Caja blanca, rama "modo remoto": acepta cualquier base de NCBI."""
    resultado = BlastSimulado(demora_segundos=0)(armar_comando("swissprot", "-remote"), ">q\nM", None, None)

    assert resultado.codigo == 0


def test_el_simulado_puede_agregar_un_campo_desconocido():
    """CP-41 · Caja blanca, rama "campo nuevo" (sirve para mostrar EC-02 en la aplicación)."""
    resultado = BlastSimulado(demora_segundos=0, campo_nuevo=True)(
        armar_comando("proteinas_demo"), ">q\nM", None, None
    )

    assert "<Hsp_nuevo-campo>" in resultado.salida


def test_ejecutar_subproceso_devuelve_codigo_salida_y_errores():
    """CP-42 · Caja blanca, ejecutar_subproceso: entrada estándar, salida, errores y código del
    proceso.
    """
    programa = "import sys; print(sys.stdin.read().upper()); print('aviso', file=sys.stderr); sys.exit(3)"

    resultado = ejecutar_subproceso([sys.executable, "-c", programa], "mkt", None, 30)

    assert (resultado.codigo, resultado.salida.strip(), resultado.errores.strip()) == (3, "MKT", "aviso")
