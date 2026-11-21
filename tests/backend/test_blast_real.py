"""Prueba de integración opcional con el BLAST+ instalado en la máquina.

Se omite si `blastp` no está en el PATH o si no se creó la base de demostración
(`bash scripts/crear_base_demo.sh`). No reemplaza a las pruebas unitarias: comprueba que
el adaptador entiende la salida real de BLAST+.
"""

import shutil
from pathlib import Path

import pytest

from backend.adaptador_blast.adaptador_blast import ErrorBlast
from backend.adaptador_blast.adaptador_blast_cli import AdaptadorBlastCli

RAIZ = Path(__file__).resolve().parents[2]
BASE_DEMO = RAIZ / "datos" / "blastdb" / "proteinas_demo.pin"

pytestmark = [
    pytest.mark.blast_real,
    pytest.mark.skipif(shutil.which("blastp") is None, reason="BLAST+ no está instalado"),
    pytest.mark.skipif(not BASE_DEMO.exists(), reason="falta la base de demostración"),
]


def leer_query_demo() -> str:
    """Lee la query FASTA de demostración."""
    return (RAIZ / "datos" / "ejemplo" / "proteina_demo.fasta").read_text(encoding="utf-8")


def test_blastp_real_sobre_la_base_de_demostracion():
    """CP-55 · Integración · CA-02 con BLAST+ real: el adaptador lee la salida real."""
    hits = AdaptadorBlastCli(directorio_trabajo=RAIZ).ejecutar(
        "blastp", leer_query_demo(), "datos/blastdb/proteinas_demo", False, {"evalue": 10}
    )

    assert len(hits) == 15
    assert hits[0]["id_hit"] == "demo_var01"
    assert hits[0]["identidades"] / hits[0]["longitud_alineamiento"] > 0.99


def test_blastp_real_con_una_base_inexistente():
    """CP-56 · Integración · R4 con BLAST+ real: una base inexistente produce ErrorBlast con el
    mensaje de BLAST+.
    """
    with pytest.raises(ErrorBlast, match="BLAST Database error"):
        AdaptadorBlastCli(directorio_trabajo=RAIZ).ejecutar(
            "blastp", leer_query_demo(), "datos/blastdb/no_existe", False, {}
        )
