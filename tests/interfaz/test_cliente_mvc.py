"""Aplicación cliente (MVC) sin la pantalla: ControladorBusqueda, Modelos y ClienteBackend.

CA-01 (la ejecución no bloquea) y regla R6 (estados de la ejecución). No se
prueba a través de la interfaz gráfica: la Vista se reemplaza por los Modelos.
"""

import io
import json
import threading
import urllib.error
import urllib.request

import pytest

from interfaz.cliente.cliente_backend import ClienteBackend, ErrorEjecucion
from interfaz.cliente.controlador_busqueda import ControladorBusqueda
from interfaz.cliente.modelo_busqueda import CON_ERROR, EN_EJECUCION, FINALIZADA, LISTA, ModeloBusqueda
from interfaz.cliente.modelo_resultados import ModeloResultados

FILAS = [{"hit_id": "h1", "score": 10.0, "evalue": 1e-5, "porcentaje_identidad": 90.0,
          "porcentaje_cobertura": 80.0}]


class ClienteFalso:
    """Doble de ClienteBackend: devuelve filas o lanza ErrorEjecucion."""

    def __init__(self, filas=None, error=None, esperar: threading.Event | None = None):
        self.filas, self.error, self.esperar = filas or [], error, esperar
        self.pedidos = []

    def ejecutar_busqueda(self, configuracion):
        self.pedidos.append(configuracion)
        if self.esperar:
            self.esperar.wait(timeout=5)
        if self.error:
            raise ErrorEjecucion(self.error)
        return self.filas


class Diferido:
    """Lanzador que guarda la tarea para correrla cuando la prueba lo decida."""

    def __init__(self):
        self.tareas = []

    def __call__(self, tarea):
        self.tareas.append(tarea)

    def correr(self):
        self.tareas.pop(0)()


def armar(cliente, lanzar=None):
    modelo_busqueda, modelo_resultados = ModeloBusqueda(), ModeloResultados()
    argumentos = (modelo_busqueda, modelo_resultados, cliente) + ((lanzar,) if lanzar else ())
    controlador = ControladorBusqueda(*argumentos)
    controlador.preparar({"secuencia": "ACGT", "programa": "blastn", "base_datos": "b"})
    return controlador, modelo_busqueda, modelo_resultados


# --- ControladorBusqueda ----------------------------------------------------------------

def test_cp50_al_ejecutar_queda_en_ejecucion_antes_de_que_llegue_la_respuesta():
    lanzar = Diferido()
    controlador, modelo_busqueda, _ = armar(ClienteFalso(FILAS), lanzar)
    controlador.ejecutar()
    assert modelo_busqueda.estado() == EN_EJECUCION and len(lanzar.tareas) == 1


def test_cp51_ca01_ejecutar_no_bloquea_mientras_el_backend_trabaja():
    """CA-01 con un hilo real: ejecutar() vuelve mientras el Backend sigue sin responder."""
    backend_responde = threading.Event()
    controlador, modelo_busqueda, modelo_resultados = armar(ClienteFalso(FILAS, esperar=backend_responde))
    terminada = threading.Event()
    modelo_busqueda.suscribir(lambda: modelo_busqueda.estado() == FINALIZADA and terminada.set())

    controlador.ejecutar()
    assert modelo_busqueda.estado() == EN_EJECUCION  # la interfaz sigue disponible
    backend_responde.set()
    assert terminada.wait(timeout=5)
    assert modelo_resultados.filas() == FILAS


def test_cp52_cuando_llegan_las_filas_las_carga_y_marca_finalizada():
    lanzar = Diferido()
    cliente = ClienteFalso(FILAS)
    controlador, modelo_busqueda, modelo_resultados = armar(cliente, lanzar)
    controlador.ejecutar()
    lanzar.correr()
    assert modelo_busqueda.estado() == FINALIZADA and modelo_resultados.filas() == FILAS
    assert cliente.pedidos == [{"secuencia": "ACGT", "programa": "blastn", "base_datos": "b"}]


def test_cp53_cuando_falla_registra_el_error_y_no_carga_filas():
    lanzar = Diferido()
    controlador, modelo_busqueda, modelo_resultados = armar(ClienteFalso(error="BLAST Database error"), lanzar)
    controlador.ejecutar()
    lanzar.correr()
    assert modelo_busqueda.estado() == CON_ERROR
    assert modelo_busqueda.mensaje_error() == "BLAST Database error"
    assert modelo_resultados.filas() == []


# --- Modelos --------------------------------------------------------------------------

def test_cp54_los_modelos_avisan_cada_cambio_a_sus_suscriptores():
    modelo_busqueda, modelo_resultados, avisos = ModeloBusqueda(), ModeloResultados(), []
    modelo_busqueda.suscribir(lambda: avisos.append(modelo_busqueda.estado()))
    modelo_resultados.suscribir(lambda: avisos.append("filas"))
    modelo_busqueda.establecer_configuracion({"secuencia": "A"})
    modelo_busqueda.marcar_en_ejecucion()
    modelo_resultados.cargar(FILAS)
    modelo_busqueda.marcar_finalizada()
    assert avisos == [LISTA, EN_EJECUCION, "filas", FINALIZADA]


def test_cp55_una_nueva_ejecucion_borra_el_error_anterior():
    modelo = ModeloBusqueda()
    modelo.registrar_error("falló")
    modelo.marcar_en_ejecucion()
    assert modelo.mensaje_error() is None


# --- ClienteBackend -------------------------------------------------------------------

class RespuestaFalsa(io.BytesIO):
    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False


def error_http(codigo: int, cuerpo: bytes) -> urllib.error.HTTPError:
    return urllib.error.HTTPError("http://x", codigo, "error", {}, io.BytesIO(cuerpo))


def test_cp56_cliente_envia_la_configuracion_y_devuelve_las_filas(monkeypatch):
    pedidos = []

    def urlopen(solicitud, timeout):
        pedidos.append(solicitud)
        return RespuestaFalsa(json.dumps({"filas": FILAS}).encode())

    monkeypatch.setattr(urllib.request, "urlopen", urlopen)
    assert ClienteBackend("http://backend/").ejecutar_busqueda({"secuencia": "A"}) == FILAS
    assert pedidos[0].full_url == "http://backend/busquedas/ejecuciones"
    assert json.loads(pedidos[0].data) == {"secuencia": "A"}


@pytest.mark.parametrize(
    ("falla", "mensaje"),
    [
        (error_http(502, b'{"error": "BLAST Database error"}'), "BLAST Database error"),
        (error_http(500, b"Internal Server Error"), "código 500"),
        (urllib.error.URLError("connection refused"), "No se pudo conectar"),
    ],
    ids=["cp57_error_de_blast", "cp58_respuesta_sin_json", "cp59_backend_caido"],
)
def test_cliente_convierte_cada_falla_en_error_de_ejecucion(monkeypatch, falla, mensaje):
    def urlopen(solicitud, timeout):
        raise falla

    monkeypatch.setattr(urllib.request, "urlopen", urlopen)
    with pytest.raises(ErrorEjecucion, match=mensaje):
        ClienteBackend("http://backend").ejecutar_busqueda({})
