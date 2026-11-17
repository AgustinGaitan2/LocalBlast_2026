"""AdaptadorBlastSimulado · doble de BLAST+ usado en la demo y en EC-01."""

import time

import pytest

from aplicacion.adaptador_blast import ErrorBlast
from datos_prueba import un_hit
from infraestructura.adaptador_blast_simulado import AdaptadorBlastSimulado


def test_cp38_devuelve_los_hits_preparados_para_esa_secuencia():
    adaptador = AdaptadorBlastSimulado({"ACGT": [un_hit("h1")]}, {"b"}, hits_por_defecto=[un_hit("otro")])
    assert [h["hit_id"] for h in adaptador.ejecutar("blastn", "ACGT", "b", False, {})] == ["h1"]


def test_cp39_para_otra_secuencia_devuelve_los_hits_por_defecto():
    adaptador = AdaptadorBlastSimulado({"ACGT": [un_hit("h1")]}, {"b"}, hits_por_defecto=[un_hit("otro")])
    assert [h["hit_id"] for h in adaptador.ejecutar("blastn", "TTTT", "b", False, {})] == ["otro"]


def test_cp40_base_inexistente_termina_con_error_como_blast():
    with pytest.raises(ErrorBlast, match=r"database \[nt\]"):
        AdaptadorBlastSimulado({}, {"b"}).ejecutar("blastn", "ACGT", "nt", False, {})


def test_cp41_aplica_la_demora_de_cada_secuencia():
    adaptador = AdaptadorBlastSimulado({}, {"b"}, demora_segundos={"LENTA": 0.2})
    inicio = time.perf_counter()
    adaptador.ejecutar("blastn", "RAPIDA", "b", False, {})
    rapida = time.perf_counter() - inicio
    adaptador.ejecutar("blastn", "LENTA", "b", False, {})
    assert rapida < 0.1 and time.perf_counter() - inicio >= 0.2


def test_cp42_aplica_una_demora_fija_a_todas_las_busquedas():
    inicio = time.perf_counter()
    AdaptadorBlastSimulado({}, {"b"}, demora_segundos=0.1).ejecutar("blastn", "A", "b", False, {})
    assert time.perf_counter() - inicio >= 0.1


def test_cp60_encuentra_los_hits_aunque_la_secuencia_traiga_espacios_o_saltos_al_final():
    adaptador = AdaptadorBlastSimulado({">q\nACGT": [un_hit("h1")]}, {"b"})
    assert len(adaptador.ejecutar("blastn", ">q\nACGT\n", "b", False, {})) == 1
