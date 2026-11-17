"""Implementaciones de RepositorioHistorial · CA-03.

La versión SQL se prueba contra un archivo SQLite temporal (prueba de integración
liviana: no requiere instalar nada).
"""

import json

import pytest
from sqlalchemy import create_engine, select
from sqlalchemy.exc import IntegrityError

from datos_prueba import FECHA_FIJA, un_hit
from dominio.busqueda import Busqueda
from infraestructura.repositorio_historial_en_memoria import RepositorioHistorialEnMemoria
from infraestructura.repositorio_historial_sql import (
    RepositorioHistorialSql, tabla_alineamientos, tabla_busquedas,
)


def una_busqueda(configuracion, *hits) -> Busqueda:
    busqueda = Busqueda(configuracion, FECHA_FIJA)
    busqueda.registrar_resultados(list(hits))
    return busqueda


@pytest.fixture
def url_sqlite(tmp_path) -> str:
    return f"sqlite:///{tmp_path / 'historial.db'}"


@pytest.fixture
def repositorio_sql(url_sqlite):
    repositorio = RepositorioHistorialSql(url_sqlite)
    yield repositorio
    repositorio.cerrar()


def leer(url: str):
    motor = create_engine(url)
    with motor.connect() as conexion:
        busquedas = conexion.execute(select(tabla_busquedas)).mappings().all()
        alineamientos = conexion.execute(select(tabla_alineamientos)).mappings().all()
    motor.dispose()
    return busquedas, alineamientos


def test_cp43_en_memoria_guarda_las_busquedas_en_orden(configuracion):
    repositorio = RepositorioHistorialEnMemoria()
    primera, segunda = una_busqueda(configuracion), una_busqueda(configuracion)
    repositorio.guardar(primera)
    repositorio.guardar(segunda)
    assert repositorio.busquedas == (primera, segunda)


def test_cp44_sql_guarda_parametros_base_fecha_y_todos_los_alineamientos(configuracion, url_sqlite, repositorio_sql):
    repositorio_sql.guardar(una_busqueda(configuracion, un_hit("h1"), un_hit("h2")))
    busquedas, alineamientos = leer(url_sqlite)
    assert len(busquedas) == 1
    assert (busquedas[0]["base_datos"], busquedas[0]["fecha"]) == ("base_demo", FECHA_FIJA)
    assert json.loads(busquedas[0]["parametros"]) == configuracion["parametros"]
    assert [a["hit_id"] for a in alineamientos] == ["h1", "h2"]
    assert {a["busqueda_id"] for a in alineamientos} == {busquedas[0]["id"]}


def test_cp45_sql_guarda_una_busqueda_sin_hits(configuracion, url_sqlite, repositorio_sql):
    repositorio_sql.guardar(una_busqueda(configuracion))
    busquedas, alineamientos = leer(url_sqlite)
    assert len(busquedas) == 1 and alineamientos == []


def test_cp46_sql_si_falla_un_alineamiento_no_queda_nada_de_la_busqueda(configuracion, url_sqlite,
                                                                       repositorio_sql):
    busqueda = una_busqueda(configuracion, un_hit("h1"))
    busqueda.alineamientos[0].hit_id = None  # viola NOT NULL
    with pytest.raises(IntegrityError):
        repositorio_sql.guardar(busqueda)
    assert leer(url_sqlite) == ([], [])
