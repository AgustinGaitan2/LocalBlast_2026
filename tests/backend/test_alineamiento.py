"""Entidad Alineamiento: regla R1 (porcentajes de identidad y de cobertura), CA-02."""

import pytest

from backend.ejecucion.alineamiento import Alineamiento
from conftest import crear_hit


@pytest.mark.parametrize(
    ("identidades", "esperado"),
    [(300, 100.0), (299, 299 / 300 * 100), (0, 0.0)],
    ids=["todas-identicas", "una-distinta", "ninguna-identica"],
)
def test_porcentaje_identidad_es_identidades_sobre_longitud_del_alineamiento(identidades, esperado):
    """CP-04 · Caja negra, valores límite · CA-02 (% identidad). El alineamiento (300) es más corto
    que la query (420): así la prueba distingue el divisor correcto.
    """
    alineamiento = Alineamiento(crear_hit(identidades=identidades, longitud_alineamiento=300), 420)

    assert alineamiento.calcular_porcentaje_identidad() == pytest.approx(esperado)


@pytest.mark.parametrize(
    ("desde", "hasta", "esperado"),
    [
        (1, 420, 100.0),         # cubre toda la query
        (1, 210, 50.0),          # cubre la mitad
        (420, 211, 50.0),        # tramo informado al revés (marcos negativos de blastx)
        (1, 1, 1 / 420 * 100),   # límite inferior: un solo residuo
        (1, 430, 100.0),         # límite superior: no puede pasar de 100 %
    ],
    ids=["completa", "mitad", "invertida", "un-residuo", "tope-100"],
)
def test_porcentaje_cobertura_es_tramo_de_la_query_sobre_su_longitud(desde, hasta, esperado):
    """CP-05 · Caja negra, clases de equivalencia y valores límite · CA-02 (% cobertura)."""
    alineamiento = Alineamiento(crear_hit(query_desde=desde, query_hasta=hasta), 420)

    assert alineamiento.calcular_porcentaje_cobertura() == pytest.approx(esperado)


@pytest.mark.parametrize(
    ("hit", "longitud_query"),
    [(crear_hit(longitud_alineamiento=0), 420), (crear_hit(), 0)],
    ids=["alineamiento-de-largo-0", "query-de-largo-0"],
)
def test_no_se_crea_un_alineamiento_con_longitudes_en_cero(hit, longitud_query):
    """CP-06 · Caja negra, valores límite inválidos · CA-02 (y caja blanca de
    Alineamiento.__init__).
    """
    with pytest.raises(ValueError):
        Alineamiento(hit, longitud_query)
