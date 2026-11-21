"""ControladorEjecucion: Secuencias 1 y 2 del diseño detallado (CA-02, CA-03, R3 y R4)."""

import pytest

from backend.acceso_datos.repositorio_historial import RepositorioHistorial
from backend.adaptador_blast.adaptador_blast import ErrorBlast
from backend.ejecucion.controlador_ejecucion import ControladorEjecucion
from conftest import FECHA_FIJA, AdaptadorDoble, crear_hit

COLUMNAS = {"id_hit", "descripcion", "score", "evalue", "porcentaje_identidad", "porcentaje_cobertura"}


def test_devuelve_una_fila_por_hit_con_las_columnas_de_la_tabla(armar_controlador, configuracion):
    """CP-03 · Caja negra · CA-02: una fila por hit, con las columnas de la tabla y en el orden de
    BLAST+.
    """
    hits = [crear_hit(id_hit="h1", score=900.0), crear_hit(id_hit="h2", score=500.0, identidades=210)]
    controlador = armar_controlador(AdaptadorDoble(hits))

    filas = controlador.ejecutar_busqueda(configuracion)

    assert [fila["id_hit"] for fila in filas] == ["h1", "h2"]
    assert all(set(fila) == COLUMNAS for fila in filas)
    assert filas[1]["porcentaje_identidad"] == pytest.approx(50.0)


def test_sin_hits_devuelve_tabla_vacia_y_la_busqueda_igual_se_guarda(
    armar_controlador, configuracion, repositorio
):
    """CP-08 · Caja negra, clase "BLAST+ sin hits" · CA-02 y CA-03."""
    filas = armar_controlador(AdaptadorDoble(hits=[])).ejecutar_busqueda(configuracion)

    assert filas == []
    assert len(repositorio.busquedas_guardadas) == 1
    assert repositorio.busquedas_guardadas[0].alineamientos == ()


def test_guarda_la_busqueda_completa_en_el_historial(armar_controlador, configuracion, repositorio):
    """CP-09 · Caja negra · CA-03: el historial recibe parámetros, base, fecha y todos los
    alineamientos crudos.
    """
    hits = [crear_hit(id_hit=f"h{i}", identidades=i) for i in range(1, 16)]  # 15 hits, varios "malos"
    armar_controlador(AdaptadorDoble(hits)).ejecutar_busqueda(configuracion)

    (guardada,) = repositorio.busquedas_guardadas
    assert guardada.parametros == configuracion["parametros"]
    assert guardada.base_datos == configuracion["base_datos"]
    assert guardada.fecha == FECHA_FIJA
    assert [a.id_hit for a in guardada.alineamientos] == [f"h{i}" for i in range(1, 16)]


def test_si_el_historial_falla_no_se_devuelve_la_tabla(configuracion):
    """CP-10 · Caja negra · CA-03 y R3: si no se pudo guardar, no se devuelve ninguna tabla."""
    class RepositorioQueFalla(RepositorioHistorial):
        """Doble de RepositorioHistorial que siempre falla al guardar."""

        def guardar(self, busqueda):
            """Simula un error de escritura en el historial."""
            raise OSError("disco lleno")

    controlador = ControladorEjecucion(AdaptadorDoble(), RepositorioQueFalla(), lambda: FECHA_FIJA)

    with pytest.raises(OSError):
        controlador.ejecutar_busqueda(configuracion)


def test_si_blast_falla_se_propaga_el_error_y_no_se_guarda_nada(
    armar_controlador, configuracion, repositorio
):
    """CP-13 · Caja negra · R4 (garantía mínima de CU004): si BLAST+ falla, el error sigue y no se
    guarda nada.
    """
    controlador = armar_controlador(AdaptadorDoble(error="BLAST Database error: sin base"))

    with pytest.raises(ErrorBlast, match="BLAST Database error: sin base"):
        controlador.ejecutar_busqueda(configuracion)
    assert repositorio.busquedas_guardadas == ()


def test_invoca_a_blast_con_la_configuracion_recibida(armar_controlador, configuracion):
    """CP-59 · Caja negra · CA-02: BLAST+ se invoca con la configuración validada recibida."""
    adaptador = AdaptadorDoble()
    armar_controlador(adaptador).ejecutar_busqueda({**configuracion, "modo": "remoto"})

    assert adaptador.llamadas == [(
        "blastp", configuracion["secuencia"], configuracion["base_datos"], True,
        configuracion["parametros"],
    )]
