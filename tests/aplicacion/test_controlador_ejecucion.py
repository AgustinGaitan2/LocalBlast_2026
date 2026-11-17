"""ControladorEjecucion · CA-02, CA-03, camino de error (R4) y EC-01.

Los colaboradores son dobles: AdaptadorBlastSimulado y el repositorio en memoria.
"""

import random
from concurrent.futures import ThreadPoolExecutor

import pytest

from aplicacion.adaptador_blast import ErrorBlast
from aplicacion.controlador_ejecucion import ControladorEjecucion
from aplicacion.repositorio_historial import RepositorioHistorial
from datos_prueba import FECHA_FIJA, un_hit, una_configuracion
from infraestructura.adaptador_blast_simulado import AdaptadorBlastSimulado
from infraestructura.repositorio_historial_en_memoria import RepositorioHistorialEnMemoria


def armar(hits: list[dict] | None = None, bases: set[str] | None = None):
    adaptador = AdaptadorBlastSimulado({}, bases or {"base_demo"}, hits_por_defecto=hits or [])
    historial = RepositorioHistorialEnMemoria()
    return ControladorEjecucion(adaptador, historial, reloj=lambda: FECHA_FIJA), adaptador, historial


class RepositorioQueFalla(RepositorioHistorial):
    def guardar(self, busqueda) -> None:
        raise RuntimeError("la base de datos no responde")


def test_cp15_devuelve_una_fila_por_hit_con_las_columnas_de_ca02(configuracion):
    controlador, _, _ = armar([un_hit("h1"), un_hit("h2")])
    filas = controlador.ejecutar_busqueda(configuracion)
    assert [f["hit_id"] for f in filas] == ["h1", "h2"]
    assert set(filas[0]) >= {"hit_id", "score", "evalue", "porcentaje_identidad", "porcentaje_cobertura"}


def test_cp16_le_pasa_al_adaptador_la_configuracion_de_la_busqueda():
    controlador, adaptador, _ = armar()
    controlador.ejecutar_busqueda(una_configuracion("ACGT", remota=True, parametros={"evalue": "10"}))
    assert adaptador.invocaciones == [{"programa": "blastn", "secuencia": "ACGT", "base_datos": "base_demo",
                                       "remota": True, "parametros": {"evalue": "10"}}]


def test_cp17_guarda_en_el_historial_la_configuracion_la_fecha_y_todos_los_hits_crudos(configuracion):
    controlador, _, historial = armar([un_hit("h1"), un_hit("h2", evalue="5.0")])
    controlador.ejecutar_busqueda(configuracion)
    (guardada,) = historial.busquedas
    assert (guardada.programa, guardada.base_datos, guardada.fecha) == ("blastn", "base_demo", FECHA_FIJA)
    assert guardada.parametros == configuracion["parametros"]
    assert [a.hit_id for a in guardada.alineamientos] == ["h1", "h2"]


def test_cp18_si_no_se_puede_guardar_no_devuelve_tabla(configuracion):
    adaptador = AdaptadorBlastSimulado({}, {"base_demo"}, hits_por_defecto=[un_hit()])
    controlador = ControladorEjecucion(adaptador, RepositorioQueFalla())
    with pytest.raises(RuntimeError):
        controlador.ejecutar_busqueda(configuracion)


def test_cp19_si_blast_falla_propaga_el_error_y_no_guarda_nada():
    controlador, _, historial = armar([un_hit()], bases={"base_demo"})
    with pytest.raises(ErrorBlast, match="No alias or index file"):
        controlador.ejecutar_busqueda(una_configuracion(base_datos="inexistente"))
    assert historial.busquedas == ()


def test_cp20_una_query_sin_residuos_no_llega_a_blast(configuracion):
    controlador, adaptador, historial = armar()
    with pytest.raises(ValueError):
        controlador.ejecutar_busqueda(una_configuracion(">vacia\n"))
    assert adaptador.invocaciones == [] and historial.busquedas == ()


def test_cp21_ec01_cinco_busquedas_simultaneas_sin_cruce_de_resultados():
    """EC-01: cinco búsquedas a la vez, con demoras distintas, reciben solo sus hits."""
    secuencias = [f">q{i}\n" + "ACGT" * (10 + i) for i in range(5)]
    hits = {s: [un_hit(f"q{i}-hit{j}") for j in range(3)] for i, s in enumerate(secuencias)}
    demoras = {s: random.Random(i).uniform(0.05, 0.3) for i, s in enumerate(secuencias)}
    historial = RepositorioHistorialEnMemoria()
    controlador = ControladorEjecucion(AdaptadorBlastSimulado(hits, {"base_demo"}, demoras), historial)

    with ThreadPoolExecutor(max_workers=5) as hilos:
        resultados = list(hilos.map(lambda s: controlador.ejecutar_busqueda(una_configuracion(s)), secuencias))

    for i, filas in enumerate(resultados):
        assert [f["hit_id"] for f in filas] == [f"q{i}-hit{j}" for j in range(3)]
    assert len(historial.busquedas) == 5
    for busqueda in historial.busquedas:
        assert [a.hit_id for a in busqueda.alineamientos] == [h["hit_id"] for h in hits[busqueda.secuencia]]
