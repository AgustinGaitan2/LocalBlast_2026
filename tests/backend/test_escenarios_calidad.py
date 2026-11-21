"""Medidas de los escenarios de calidad que alcanzan a la HU (EC-01 y EC-02)."""

import random
import sqlite3
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from contextlib import closing

import pytest

from backend.acceso_datos.conexion_bd import ConexionBD
from backend.acceso_datos.repositorio_historial_sqlite import RepositorioHistorialSqlite
from backend.adaptador_blast.adaptador_blast import ErrorBlast
from backend.adaptador_blast.adaptador_blast_cli import AdaptadorBlastCli, ResultadoComando
from backend.ejecucion.controlador_ejecucion import ControladorEjecucion
from conftest import FECHA_FIJA, armar_salida_xml

BUSQUEDAS_SIMULTANEAS = 5


class BlastConDemoras:
    """Hace de BLAST+: cada invocación tarda distinto y devuelve hits que identifican a su query.

    La barrera obliga a que las cinco invocaciones estén en curso al mismo tiempo: si el sistema
    las atendiera de a una, la barrera vencería y la prueba fallaría.
    """

    def __init__(self) -> None:
        """Prepara la barrera para las cinco invocaciones y las demoras al azar."""
        self._barrera = threading.Barrier(BUSQUEDAS_SIMULTANEAS, timeout=10)
        self._azar = random.Random(2026)

    def __call__(self, comando, entrada, directorio, limite_segundos):
        """Espera a las demás invocaciones, demora un tiempo al azar y devuelve hits de su query."""
        nombre = entrada.splitlines()[0][1:]  # ">query3" -> "query3"
        self._barrera.wait()
        time.sleep(self._azar.uniform(0.05, 0.4))
        hits = [{"id": f"{nombre}_hit{i}", "def": f"Hit {i} de {nombre}"} for i in range(1, 4)]
        return ResultadoComando(0, armar_salida_xml(*hits), "")


def test_cinco_busquedas_simultaneas_no_mezclan_sus_resultados(tmp_path, configuracion):
    """CP-18 · Caja negra · EC-01: cinco búsquedas a la vez, cero cruces de resultados."""
    repositorio = RepositorioHistorialSqlite(ConexionBD(tmp_path / "historial.sqlite3"))
    adaptador = AdaptadorBlastCli(BlastConDemoras())
    controlador = ControladorEjecucion(adaptador, repositorio, reloj=lambda: FECHA_FIJA)
    consultas = [f"query{n}" for n in range(1, BUSQUEDAS_SIMULTANEAS + 1)]

    def ejecutar(nombre):
        """Ejecuta una búsqueda cuya query se llama como indica el nombre."""
        return controlador.ejecutar_busqueda({**configuracion, "secuencia": f">{nombre}\nMKTAAV\n"})

    with ThreadPoolExecutor(max_workers=BUSQUEDAS_SIMULTANEAS) as hilos:
        resultados = dict(zip(consultas, hilos.map(ejecutar, consultas)))

    for nombre, filas in resultados.items():
        assert [fila["id_hit"] for fila in filas] == [f"{nombre}_hit{i}" for i in range(1, 4)]
    guardados = _leer_alineamientos_guardados_por_query(tmp_path / "historial.sqlite3")
    assert guardados == {nombre: [f"{nombre}_hit{i}" for i in range(1, 4)] for nombre in consultas}


def _leer_alineamientos_guardados_por_query(ruta) -> dict[str, list[str]]:
    """Lee del historial SQLite los ids de hit guardados para cada query."""
    with closing(sqlite3.connect(ruta)) as conexion:
        filas = conexion.execute(
            "SELECT b.secuencia, a.id_hit FROM alineamiento a JOIN busqueda b ON b.id = a.busqueda_id "
            "ORDER BY a.busqueda_id, a.orden"
        ).fetchall()
    guardados: dict[str, list[str]] = {}
    for secuencia, id_hit in filas:
        guardados.setdefault(secuencia.splitlines()[0][1:], []).append(id_hit)
    return guardados


def test_los_campos_desconocidos_no_alteran_los_hits_y_se_advierten(caplog):
    """CP-19 · Caja negra · EC-02: campos desconocidos se ignoran y se advierten, los conocidos
    llegan intactos.
    """
    hits = [{"id": "h1", "ident": 419}, {"id": "h2", "ident": 300, "evalue": 3e-50}]
    sin_cambios = AdaptadorBlastCli().leer_salida(armar_salida_xml(*hits))

    con_campos_nuevos = AdaptadorBlastCli().leer_salida(armar_salida_xml(
        *hits,
        campos_extra_hsp="<Hsp_nuevo-campo>7</Hsp_nuevo-campo>",
        campos_extra_hit="<Hit_taxid>562</Hit_taxid>",
    ))

    assert con_campos_nuevos == sin_cambios
    assert len(caplog.records) == 1
    assert caplog.records[0].levelname == "WARNING"
    assert "Hit_taxid, Hsp_nuevo-campo" in caplog.records[0].getMessage()


@pytest.mark.parametrize("campo", ["Hsp_evalue", "Hsp_identity", "Hit_id"])
def test_si_falta_un_campo_obligatorio_lanza_error_blast_que_lo_nombra(campo):
    """CP-20 · Caja negra, valor límite de EC-02: si falta un campo obligatorio, no se inventa el
    dato.
    """
    xml = armar_salida_xml({"id": "h1"})
    inicio = xml.index(f"<{campo}>")
    fin = xml.index(f"</{campo}>") + len(f"</{campo}>")

    with pytest.raises(ErrorBlast, match=f"campo obligatorio {campo}"):
        AdaptadorBlastCli().leer_salida(xml[:inicio] + xml[fin:])
