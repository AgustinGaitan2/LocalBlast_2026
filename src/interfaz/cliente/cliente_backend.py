"""ClienteBackend (Aplicación Web, componente Cliente del Backend).

Único punto del cliente que conoce la interfaz REST del Backend. Usa solo la
biblioteca estándar (urllib) para no sumar dependencias.
"""

import json
import urllib.error
import urllib.request


class ErrorEjecucion(Exception):
    """El Backend no devolvió resultados: BLAST+ falló o no se pudo conectar."""

    def __init__(self, mensaje: str) -> None:
        super().__init__(mensaje)
        self.mensaje = mensaje


class ClienteBackend:
    def __init__(self, url_base: str, tiempo_maximo_segundos: float = 3600) -> None:
        self.url_base = url_base.rstrip("/")
        self.tiempo_maximo_segundos = tiempo_maximo_segundos

    def ejecutar_busqueda(self, configuracion: dict) -> list[dict]:
        solicitud = urllib.request.Request(
            f"{self.url_base}/busquedas/ejecuciones",
            data=json.dumps(configuracion).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(solicitud, timeout=self.tiempo_maximo_segundos) as respuesta:
                return json.loads(respuesta.read())["filas"]
        except urllib.error.HTTPError as error:
            raise ErrorEjecucion(self._mensaje_de(error)) from error
        except (urllib.error.URLError, TimeoutError) as error:
            raise ErrorEjecucion(f"No se pudo conectar con el Backend en {self.url_base}.") from error

    @staticmethod
    def _mensaje_de(error: urllib.error.HTTPError) -> str:
        try:
            return json.loads(error.read())["error"]
        except (ValueError, KeyError, TypeError):
            return f"El Backend respondió con el código {error.code}."
