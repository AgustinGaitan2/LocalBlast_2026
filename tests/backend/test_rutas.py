"""Componente Controladores: la ruta HTTP traduce la solicitud y la respuesta, sin lógica propia."""

import pytest
from fastapi.testclient import TestClient

from backend.controladores.rutas import crear_app
from backend.ejecucion.controlador_ejecucion import ErrorBlast

RUTA = "/api/busquedas/ejecucion"
SOLICITUD = {
    "secuencia": ">q\nMKT",
    "variante": "blastp",
    "modo": "local",
    "base_datos": "base",
    "parametros": {"evalue": 10, "matrix": "BLOSUM62"},
    "query_nombre": "campo que solo usa la interfaz",
}


class ControladorDoble:
    """Doble de ControladorEjecucion: registra lo recibido y devuelve filas fijas o lanza ErrorBlast."""

    def __init__(self, filas=None, error=None):
        """Configura las filas que devolverá o el error que lanzará."""
        self.filas, self.error, self.recibido = filas or [], error, None

    def ejecutar_busqueda(self, configuracion):
        """Registra la configuración recibida y responde lo configurado."""
        self.recibido = configuracion
        if self.error:
            raise ErrorBlast(self.error)
        return self.filas


def test_una_busqueda_exitosa_responde_las_filas():
    """CP-16 · Caja negra · CA-02: una búsqueda que termina bien responde 200 con las filas."""
    controlador = ControladorDoble(filas=[{"id_hit": "h1"}])

    respuesta = TestClient(crear_app(controlador)).post(RUTA, json=SOLICITUD)

    assert (respuesta.status_code, respuesta.json()) == (200, {"filas": [{"id_hit": "h1"}]})
    assert "query_nombre" not in controlador.recibido


def test_un_error_de_blast_responde_502_con_el_mensaje_literal():
    """CP-15 · Caja negra · R4: si BLAST+ falla, responde 502 con el mensaje literal."""
    controlador = ControladorDoble(error="BLAST Database error: x")

    respuesta = TestClient(crear_app(controlador)).post(RUTA, json=SOLICITUD)

    assert respuesta.status_code == 502
    assert respuesta.json() == {"tipo": "ErrorBlast", "mensaje": "BLAST Database error: x"}


@pytest.mark.parametrize(
    "cambio",
    [{"variante": "rm"}, {"modo": "nube"}, {"secuencia": ""}, {"base_datos": None}],
    ids=["variante", "modo", "secuencia-vacia", "sin-base"],
)
def test_una_solicitud_mal_formada_se_rechaza_con_422(cambio):
    """CP-17 · Caja negra, clases inválidas de la solicitud: responde 422 y no llega al
    controlador.
    """
    controlador = ControladorDoble()

    respuesta = TestClient(crear_app(controlador)).post(RUTA, json={**SOLICITUD, **cambio})

    assert respuesta.status_code == 422
    assert controlador.recibido is None


@pytest.mark.parametrize(("con_index", "esperado"), [(True, 200), (False, 404)])
def test_sirve_la_interfaz_compilada_solo_si_existe(tmp_path, con_index, esperado):
    """CP-44 · Caja blanca, crear_app: sirve la interfaz compilada solo si existe."""
    if con_index:
        (tmp_path / "index.html").write_text("<h1>LocalBlast</h1>", encoding="utf-8")

    respuesta = TestClient(crear_app(ControladorDoble(), carpeta_web=tmp_path)).get("/")

    assert respuesta.status_code == esperado
