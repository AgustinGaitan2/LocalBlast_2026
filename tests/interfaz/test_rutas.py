"""Ruta HTTP de ejecución (componente Controladores): traduce JSON <-> controlador."""

import pytest
from fastapi.testclient import TestClient

from aplicacion.controlador_ejecucion import ControladorEjecucion
from datos_prueba import un_hit, una_configuracion
from infraestructura.adaptador_blast_simulado import AdaptadorBlastSimulado
from infraestructura.repositorio_historial_en_memoria import RepositorioHistorialEnMemoria
from interfaz.rutas import crear_app

URL = "/busquedas/ejecuciones"


@pytest.fixture
def cliente_http():
    adaptador = AdaptadorBlastSimulado({}, {"base_demo"}, hits_por_defecto=[un_hit("h1")])
    controlador = ControladorEjecucion(adaptador, RepositorioHistorialEnMemoria())
    return TestClient(crear_app(controlador))


def test_cp47_responde_200_con_las_filas_de_la_tabla(cliente_http):
    respuesta = cliente_http.post(URL, json=una_configuracion())
    assert respuesta.status_code == 200
    assert [f["hit_id"] for f in respuesta.json()["filas"]] == ["h1"]


def test_cp48_error_de_blast_responde_502_con_el_mensaje(cliente_http):
    respuesta = cliente_http.post(URL, json=una_configuracion(base_datos="nt"))
    assert respuesta.status_code == 502
    assert "No alias or index file" in respuesta.json()["error"]


def test_cp49_query_sin_residuos_responde_422(cliente_http):
    respuesta = cliente_http.post(URL, json=una_configuracion(">vacia\n"))
    assert respuesta.status_code == 422
    assert "residuos" in respuesta.json()["error"]
