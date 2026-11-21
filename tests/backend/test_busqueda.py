"""Entidad Busqueda: raíz del agregado y regla R2 (el conjunto crudo completo)."""

import pytest

from backend.ejecucion.busqueda import Busqueda
from conftest import FECHA_FIJA, QUERY_420, crear_hit


def crear_busqueda(**cambios) -> Busqueda:
    """Crea una búsqueda válida, cambiando los campos de configuración indicados."""
    configuracion = {
        "secuencia": QUERY_420,
        "variante": "blastp",
        "modo": "local",
        "base_datos": "base",
        "parametros": {"evalue": 10},
    }
    configuracion.update(cambios)
    return Busqueda(configuracion, FECHA_FIJA)


def test_los_resultados_se_registran_una_sola_vez():
    """CP-34 · Caja blanca, Busqueda.registrar_resultados (rama "ya registrados") · R2."""
    busqueda = crear_busqueda()
    busqueda.registrar_resultados([crear_hit(id_hit="a"), crear_hit(id_hit="b")])

    with pytest.raises(ValueError):
        busqueda.registrar_resultados([crear_hit(id_hit="c")])
    assert [a.id_hit for a in busqueda.alineamientos] == ["a", "b"]


@pytest.mark.parametrize("parametros", [None, {}], ids=["nulos", "vacios"])
def test_una_busqueda_sin_parametros_los_toma_como_vacios(parametros):
    """CP-35 · Caja blanca, Busqueda.__init__ (rama "sin parámetros")."""
    assert crear_busqueda(parametros=parametros).parametros == {}


@pytest.mark.parametrize(
    ("secuencia", "esperada"),
    [(QUERY_420, 420), (">q con espacios\nMKT AAV\n  GGL\n", 9), ("MKTAAV\nGGL", 9), ("", 0)],
    ids=["fasta-multilinea", "con-espacios", "sin-encabezado", "vacia"],
)
def test_la_longitud_de_la_query_cuenta_solo_residuos(secuencia, esperada):
    """CP-36 · Caja blanca, Busqueda.longitud_query (con y sin encabezado FASTA)."""
    assert crear_busqueda(secuencia=secuencia).longitud_query == esperada


@pytest.mark.parametrize(("modo", "esperado"), [("remoto", True), ("local", False)])
def test_la_busqueda_es_remota_solo_en_modo_remoto(modo, esperado):
    """CP-37 · Caja blanca, Busqueda.es_remota."""
    assert crear_busqueda(modo=modo).es_remota is esperado
