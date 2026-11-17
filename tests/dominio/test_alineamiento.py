"""Entidad Alineamiento · regla R1 (CA-02)."""

import pytest

from datos_prueba import un_hit
from dominio.alineamiento import Alineamiento


def test_cp01_porcentaje_identidad_es_identidades_sobre_longitud_del_alineamiento():
    alineamiento = Alineamiento(un_hit(identidades="90", longitud_alineamiento="120"), longitud_query=200)
    assert alineamiento.porcentaje_identidad() == pytest.approx(75.0)


def test_cp02_identidad_completa_da_cien_por_ciento():
    alineamiento = Alineamiento(un_hit(identidades="100", longitud_alineamiento="100"), longitud_query=100)
    assert alineamiento.porcentaje_identidad() == pytest.approx(100.0)


def test_cp03_cobertura_cuenta_el_tramo_inclusivo_de_la_query():
    alineamiento = Alineamiento(un_hit(query_desde="11", query_hasta="60"), longitud_query=100)
    assert alineamiento.porcentaje_cobertura() == pytest.approx(50.0)


def test_cp04_query_cubierta_de_punta_a_punta_da_cien_por_ciento():
    alineamiento = Alineamiento(un_hit(query_desde="1", query_hasta="250"), longitud_query=250)
    assert alineamiento.porcentaje_cobertura() == pytest.approx(100.0)


def test_cp05_convierte_los_datos_del_hit_a_sus_tipos():
    alineamiento = Alineamiento(un_hit("XM_1", score="88.2", evalue="3e-10"), longitud_query=100)
    assert (alineamiento.hit_id, alineamiento.score, alineamiento.evalue) == ("XM_1", 88.2, 3e-10)
