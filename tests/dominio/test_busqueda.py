"""Entidad Busqueda · reglas R1 y R2, CA-02 y CA-03."""

import pytest

from datos_prueba import FECHA_FIJA, un_hit, una_configuracion
from dominio.busqueda import Busqueda


def test_cp06_toma_la_configuracion_validada_y_la_fecha(configuracion):
    busqueda = Busqueda(configuracion, FECHA_FIJA)
    assert (busqueda.programa, busqueda.base_datos, busqueda.remota) == ("blastn", "base_demo", False)
    assert busqueda.parametros == {"evalue": "0.001", "word_size": "11"}
    assert busqueda.fecha == FECHA_FIJA
    assert busqueda.alineamientos == []


def test_cp07_sin_modo_ni_parametros_usa_local_y_parametros_vacios():
    busqueda = Busqueda({"secuencia": "ACGT", "programa": "blastn", "base_datos": "b"}, FECHA_FIJA)
    assert busqueda.remota is False and busqueda.parametros == {}


def test_cp08_longitud_de_query_fasta_ignora_encabezado_y_saltos_de_linea():
    busqueda = Busqueda(una_configuracion(">q1 gen X\nACGTA\nCGT \n"), FECHA_FIJA)
    assert busqueda.longitud_query() == 8


def test_cp09_longitud_de_query_en_texto_plano():
    assert Busqueda(una_configuracion("MKV LLA"), FECHA_FIJA).longitud_query() == 6


def test_cp10_rechaza_una_query_sin_residuos():
    with pytest.raises(ValueError, match="no tiene residuos"):
        Busqueda(una_configuracion(">solo encabezado\n"), FECHA_FIJA)


def test_cp11_crea_un_alineamiento_por_cada_hit_sin_descartar_ninguno(configuracion):
    busqueda = Busqueda(configuracion, FECHA_FIJA)
    hits = [un_hit("h1"), un_hit("h2", evalue="9.9"), un_hit("h3", identidades="1")]
    busqueda.registrar_resultados(hits)
    assert [a.hit_id for a in busqueda.alineamientos] == ["h1", "h2", "h3"]


def test_cp12_cada_alineamiento_recibe_la_longitud_de_la_query(configuracion):
    busqueda = Busqueda(configuracion, FECHA_FIJA)
    busqueda.registrar_resultados([un_hit(query_desde="1", query_hasta="25")])
    assert busqueda.alineamientos[0].porcentaje_cobertura() == pytest.approx(25.0)


def test_cp13_sin_hits_no_hay_alineamientos_ni_filas(configuracion):
    busqueda = Busqueda(configuracion, FECHA_FIJA)
    busqueda.registrar_resultados([])
    assert busqueda.tabla_resultados() == []


def test_cp14_la_tabla_tiene_las_columnas_de_ca02(configuracion):
    busqueda = Busqueda(configuracion, FECHA_FIJA)
    busqueda.registrar_resultados([un_hit("h1", identidades="2", longitud_alineamiento="3",
                                          query_desde="1", query_hasta="30")])
    assert busqueda.tabla_resultados() == [
        {"hit_id": "h1", "descripcion": "descripción de h1", "score": 200.5, "evalue": 1e-50,
         "porcentaje_identidad": 66.67, "porcentaje_cobertura": 30.0}
    ]
