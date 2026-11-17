"""Punto de arranque de LocalBlast (HU08_CU004_B).

Es el único lugar que elige las implementaciones concretas y se las pasa por
constructor a quien las usa (inyección de dependencias, decisión D9). Cambiar el
historial en memoria por SQLite o PostgreSQL, o BLAST+ real por el simulado, es
cambiar un argumento acá: el controlador no se modifica.

Uso:
    python src/main.py                 # Backend + interfaz gráfica (demo)
    python src/main.py backend         # solo el Backend (API REST)
    python src/main.py --help
"""

import argparse
import logging
import shutil
import threading
import time

import uvicorn

from aplicacion.adaptador_blast import AdaptadorBlast
from aplicacion.controlador_ejecucion import ControladorEjecucion
from aplicacion.repositorio_historial import RepositorioHistorial
from infraestructura.adaptador_blast_cli import AdaptadorBlastCli
from infraestructura.adaptador_blast_simulado import AdaptadorBlastSimulado
from infraestructura.datos_demo import BASES_DEMO, HITS_DEMO, SECUENCIA_DEMO
from infraestructura.repositorio_historial_en_memoria import RepositorioHistorialEnMemoria
from infraestructura.repositorio_historial_sql import RepositorioHistorialSql
from interfaz.rutas import crear_app


def crear_adaptador(tipo: str, directorio_binarios: str, demora: float) -> AdaptadorBlast:
    if tipo == "auto":
        tipo = "cli" if shutil.which("blastn") or directorio_binarios else "simulado"
    if tipo == "cli":
        return AdaptadorBlastCli(directorio_binarios)
    return AdaptadorBlastSimulado({SECUENCIA_DEMO.strip(): HITS_DEMO}, BASES_DEMO, demora_segundos=demora)


def crear_historial(url: str) -> RepositorioHistorial:
    if url == "memoria":
        return RepositorioHistorialEnMemoria()
    return RepositorioHistorialSql(url)


def levantar_backend(controlador: ControladorEjecucion, host: str, puerto: int) -> uvicorn.Server:
    servidor = uvicorn.Server(uvicorn.Config(crear_app(controlador), host=host, port=puerto, log_level="warning"))
    threading.Thread(target=servidor.run, daemon=True).start()
    for _ in range(100):  # espera a que el Backend acepte conexiones
        if servidor.started:
            break
        time.sleep(0.05)
    return servidor


def abrir_interfaz(url_backend: str, base_inicial: str) -> None:
    import tkinter as tk

    from interfaz.cliente.cliente_backend import ClienteBackend
    from interfaz.cliente.controlador_busqueda import ControladorBusqueda
    from interfaz.cliente.modelo_busqueda import ModeloBusqueda
    from interfaz.cliente.modelo_resultados import ModeloResultados
    from interfaz.cliente.pantalla_busqueda import PantallaBusqueda

    modelo_busqueda = ModeloBusqueda()
    modelo_resultados = ModeloResultados()
    controlador = ControladorBusqueda(modelo_busqueda, modelo_resultados, ClienteBackend(url_backend))
    raiz = tk.Tk()
    PantallaBusqueda(raiz, controlador, modelo_busqueda, modelo_resultados,
                     {"secuencia": SECUENCIA_DEMO, "programa": "blastn", "base_datos": base_inicial})
    raiz.mainloop()


def main() -> None:
    parser = argparse.ArgumentParser(description="LocalBlast · HU08 Ejecutar la búsqueda y ver sus resultados")
    parser.add_argument("modo", nargs="?", choices=["app", "backend"], default="app",
                        help="app: Backend + interfaz gráfica (por defecto); backend: solo la API REST")
    parser.add_argument("--adaptador", choices=["auto", "cli", "simulado"], default="auto",
                        help="BLAST+ real (cli), simulado, o auto: real si blastn está en el PATH")
    parser.add_argument("--blast-bin", default="", help="carpeta de los binarios de BLAST+ (si no están en el PATH)")
    parser.add_argument("--historial", default="sqlite:///localblast.db",
                        help="'memoria' o una URL de SQLAlchemy (sqlite:///..., postgresql://...)")
    parser.add_argument("--demora", type=float, default=2.0,
                        help="segundos que tarda el adaptador simulado (para ver el progreso)")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--puerto", type=int, default=8000)
    argumentos = parser.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s: %(message)s")

    adaptador = crear_adaptador(argumentos.adaptador, argumentos.blast_bin, argumentos.demora)
    historial = crear_historial(argumentos.historial)
    controlador = ControladorEjecucion(adaptador, historial)
    logging.info("Adaptador: %s · Historial: %s", type(adaptador).__name__, type(historial).__name__)

    if argumentos.modo == "backend":
        uvicorn.run(crear_app(controlador), host=argumentos.host, port=argumentos.puerto)
        return
    levantar_backend(controlador, argumentos.host, argumentos.puerto)
    base_inicial = "base_demo" if isinstance(adaptador, AdaptadorBlastSimulado) else ""
    abrir_interfaz(f"http://{argumentos.host}:{argumentos.puerto}", base_inicial)


if __name__ == "__main__":
    main()
