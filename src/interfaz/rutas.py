"""Rutas HTTP del Backend (componente Controladores, capa de presentación).

Código del framework sin lógica propia: convierte la solicitud JSON en la llamada
a ``ControladorEjecucion.ejecutar_busqueda`` y el resultado (o el error) en la
respuesta JSON. La ruta es ``def`` (no ``async``) para que FastAPI atienda cada
solicitud en su propio hilo (decisión D3, EC-01).
"""

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

from aplicacion.adaptador_blast import ErrorBlast
from aplicacion.controlador_ejecucion import ControladorEjecucion


class ConfiguracionBusqueda(BaseModel):
    """Forma de la configuración validada que envía la Aplicación Web."""

    secuencia: str
    programa: str
    base_datos: str
    remota: bool = False
    parametros: dict = Field(default_factory=dict)


def crear_app(controlador: ControladorEjecucion) -> FastAPI:
    app = FastAPI(title="LocalBlast - Backend")

    @app.post("/busquedas/ejecuciones")
    def ejecutar_busqueda(configuracion: ConfiguracionBusqueda):
        try:
            filas = controlador.ejecutar_busqueda(configuracion.model_dump())
        except ErrorBlast as error:
            return JSONResponse(status_code=502, content={"error": error.mensaje})
        except ValueError as error:
            return JSONResponse(status_code=422, content={"error": str(error)})
        return {"filas": filas}

    return app
