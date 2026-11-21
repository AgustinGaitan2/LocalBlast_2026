"""Acceso a datos: RepositorioHistorialSqlite y ConexionBD (CA-03 y R7)."""

import json
import sqlite3
from contextlib import closing

import pytest

from backend.acceso_datos.conexion_bd import ConexionBD
from backend.acceso_datos.repositorio_historial_sqlite import RepositorioHistorialSqlite
from backend.ejecucion.busqueda import Busqueda
from conftest import FECHA_FIJA, QUERY_420, crear_hit


def crear_busqueda_con(hits) -> Busqueda:
    """Crea una búsqueda con los hits indicados ya registrados."""
    busqueda = Busqueda(
        {"secuencia": QUERY_420, "variante": "blastp", "modo": "local", "base_datos": "mi_base",
         "parametros": {"evalue": 10, "matrix": "BLOSUM62"}},
        FECHA_FIJA,
    )
    busqueda.registrar_resultados(hits)
    return busqueda


def consultar(ruta, sql):
    """Ejecuta una consulta sobre el archivo SQLite y devuelve todas las filas."""
    with closing(sqlite3.connect(ruta)) as conexion:
        return conexion.execute(sql).fetchall()


def test_guarda_la_busqueda_y_sus_alineamientos_en_sqlite(tmp_path):
    """CP-11 · Caja negra · CA-03: el historial guarda la búsqueda y todos sus alineamientos con
    sus valores.
    """
    ruta = tmp_path / "historial.sqlite3"
    hits = [crear_hit(id_hit="h1"), crear_hit(id_hit="h2", evalue=3e-50, identidades=300)]
    RepositorioHistorialSqlite(ConexionBD(ruta)).guardar(crear_busqueda_con(hits))

    ((fecha, variante, modo, base, secuencia, parametros),) = consultar(
        ruta, "SELECT fecha, variante, modo, base_datos, secuencia, parametros FROM busqueda"
    )
    assert (fecha, variante, modo, base, secuencia) == (
        FECHA_FIJA.isoformat(), "blastp", "local", "mi_base", QUERY_420
    )
    assert json.loads(parametros) == {"evalue": 10, "matrix": "BLOSUM62"}
    assert consultar(ruta, "SELECT orden, id_hit, evalue, identidades FROM alineamiento ORDER BY orden") == [
        (1, "h1", 0.0, 419), (2, "h2", 3e-50, 300)
    ]


def test_guarda_una_busqueda_sin_alineamientos(tmp_path):
    """CP-43 · Caja blanca, RepositorioHistorialSqlite.guardar con el ciclo de alineamientos vacío.

    """
    ruta = tmp_path / "historial.sqlite3"
    RepositorioHistorialSqlite(ConexionBD(ruta)).guardar(crear_busqueda_con([]))

    assert consultar(ruta, "SELECT COUNT(*) FROM busqueda") == [(1,)]
    assert consultar(ruta, "SELECT COUNT(*) FROM alineamiento") == [(0,)]


def test_si_una_sentencia_falla_no_se_escribe_nada(tmp_path):
    """CP-12 · Caja negra · R7: si una escritura falla, no queda nada del registro."""
    ruta = tmp_path / "historial.sqlite3"
    conexion = ConexionBD(ruta)
    registro = [
        ("INSERT INTO busqueda VALUES (?, ?, ?, ?, ?, ?, ?)", ("b1", "f", "blastp", "local", "x", "q", "{}")),
        ("INSERT INTO alineamiento (busqueda_id) VALUES (?)", ("b1",)),  # faltan columnas obligatorias
    ]

    with pytest.raises(sqlite3.IntegrityError):
        conexion.ejecutar_transaccion(registro)
    assert consultar(ruta, "SELECT COUNT(*) FROM busqueda") == [(0,)]
