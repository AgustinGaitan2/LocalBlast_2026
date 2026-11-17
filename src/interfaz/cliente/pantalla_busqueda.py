"""PantallaBusqueda (Aplicación Web, componente Pantallas, rol Vista del MVC).

Frontera con el investigador. Solo conoce a ControladorBusqueda (para delegar) y
a los Modelos (para leerlos). No calcula, no valida ni decide: dibuja progreso,
tabla o error según lo que tengan los Modelos (regla R6).

Tkinter no admite que otro hilo toque los widgets. Los Modelos avisan sus
cambios desde el hilo que espera al Backend, así que la Vista solo anota que hay
que redibujar y el hilo de la interfaz lo hace en su próximo ciclo.
"""

import threading
import tkinter as tk
from tkinter import ttk

from interfaz.cliente.controlador_busqueda import ControladorBusqueda
from interfaz.cliente.modelo_busqueda import CON_ERROR, EN_EJECUCION, FINALIZADA, ModeloBusqueda
from interfaz.cliente.modelo_resultados import ModeloResultados

PROGRAMAS = ("blastn", "blastp", "blastx", "tblastn", "tblastx")
COLUMNAS = (
    ("hit_id", "Hit", 120),
    ("descripcion", "Descripción", 330),
    ("score", "Score (bits)", 90),
    ("evalue", "E-value", 90),
    ("porcentaje_identidad", "% identidad", 90),
    ("porcentaje_cobertura", "% cobertura", 90),
)


class PantallaBusqueda:
    def __init__(
        self,
        raiz: tk.Tk,
        controlador: ControladorBusqueda,
        modelo_busqueda: ModeloBusqueda,
        modelo_resultados: ModeloResultados,
        valores_iniciales: dict | None = None,
    ) -> None:
        self._raiz = raiz
        self._controlador = controlador
        self._modelo_busqueda = modelo_busqueda
        self._modelo_resultados = modelo_resultados
        self._hay_cambios = threading.Event()
        self._armar_formulario(valores_iniciales or {})
        modelo_busqueda.suscribir(self._hay_cambios.set)
        modelo_resultados.suscribir(self._hay_cambios.set)
        self._raiz.after(100, self._observar_modelos)

    # --- acciones del investigador -------------------------------------------------
    def presionar_ejecutar(self) -> None:
        parametros = {"evalue": self._evalue.get().strip()} if self._evalue.get().strip() else {}
        self._controlador.preparar(
            {
                "secuencia": self._secuencia.get("1.0", tk.END),
                "programa": self._programa.get(),
                "base_datos": self._base_datos.get().strip(),
                "remota": self._remota.get(),
                "parametros": parametros,
            }
        )
        self._controlador.ejecutar()

    # --- dibujo según los Modelos ---------------------------------------------------
    def _observar_modelos(self) -> None:
        if self._hay_cambios.is_set():
            self._hay_cambios.clear()
            self._redibujar()
        self._raiz.after(100, self._observar_modelos)

    def _redibujar(self) -> None:
        estado = self._modelo_busqueda.estado()
        if estado == EN_EJECUCION:
            self.mostrar_progreso()
        elif estado == FINALIZADA:
            self.mostrar_resultados(self._modelo_resultados.filas())
        elif estado == CON_ERROR:
            self.mostrar_error(self._modelo_busqueda.mensaje_error() or "")

    def mostrar_progreso(self) -> None:
        self._boton.state(["disabled"])
        self._limpiar_tabla()
        self._mensaje.configure(text="Ejecutando la búsqueda en BLAST+… podés seguir usando la aplicación.",
                                foreground="#1d4ed8")
        self._progreso.grid()
        self._progreso.start(12)

    def mostrar_resultados(self, filas: list[dict]) -> None:
        self._detener_progreso()
        self._limpiar_tabla()
        for fila in filas:
            self._tabla.insert("", tk.END, values=[fila[clave] for clave, _, _ in COLUMNAS])
        self._mensaje.configure(text=f"Búsqueda terminada y guardada en el historial: {len(filas)} alineamientos.",
                                foreground="#15803d")

    def mostrar_error(self, mensaje: str) -> None:
        self._detener_progreso()
        self._limpiar_tabla()
        self._mensaje.configure(text=f"La búsqueda no terminó bien: {mensaje}", foreground="#b91c1c")

    # --- armado de widgets -----------------------------------------------------------
    def _detener_progreso(self) -> None:
        self._progreso.stop()
        self._progreso.grid_remove()
        self._boton.state(["!disabled"])

    def _limpiar_tabla(self) -> None:
        self._tabla.delete(*self._tabla.get_children())

    def _armar_formulario(self, valores: dict) -> None:
        self._raiz.title("LocalBlast · Ejecutar búsqueda (HU08)")
        marco = ttk.Frame(self._raiz, padding=12)
        marco.grid(sticky="nsew")
        self._raiz.columnconfigure(0, weight=1)
        self._raiz.rowconfigure(0, weight=1)
        marco.columnconfigure(1, weight=1)
        marco.rowconfigure(7, weight=1)

        ttk.Label(marco, text="Secuencia query (FASTA)").grid(row=0, column=0, sticky="nw")
        self._secuencia = tk.Text(marco, height=6, width=80, font=("Courier", 10))
        self._secuencia.insert("1.0", valores.get("secuencia", ""))
        self._secuencia.grid(row=0, column=1, columnspan=3, sticky="ew", pady=(0, 6))

        ttk.Label(marco, text="Programa").grid(row=1, column=0, sticky="w")
        self._programa = ttk.Combobox(marco, values=PROGRAMAS, state="readonly", width=10)
        self._programa.set(valores.get("programa", "blastn"))
        self._programa.grid(row=1, column=1, sticky="w")

        ttk.Label(marco, text="Base de datos").grid(row=2, column=0, sticky="w")
        self._base_datos = ttk.Entry(marco, width=30)
        self._base_datos.insert(0, valores.get("base_datos", ""))
        self._base_datos.grid(row=2, column=1, sticky="w")

        ttk.Label(marco, text="E-value máximo").grid(row=3, column=0, sticky="w")
        self._evalue = ttk.Entry(marco, width=12)
        self._evalue.insert(0, valores.get("evalue", "10"))
        self._evalue.grid(row=3, column=1, sticky="w")

        self._remota = tk.BooleanVar(value=False)
        ttk.Checkbutton(marco, text="Ejecutar en modo remoto (NCBI)", variable=self._remota).grid(
            row=4, column=1, sticky="w")

        self._boton = ttk.Button(marco, text="Ejecutar búsqueda", command=self.presionar_ejecutar)
        self._boton.grid(row=5, column=0, sticky="w", pady=8)
        self._progreso = ttk.Progressbar(marco, mode="indeterminate", length=200)
        self._progreso.grid(row=5, column=1, sticky="w")
        self._progreso.grid_remove()
        self._mensaje = ttk.Label(marco, text="", wraplength=860)
        self._mensaje.grid(row=6, column=0, columnspan=4, sticky="w", pady=(0, 6))

        self._tabla = ttk.Treeview(marco, columns=[c for c, _, _ in COLUMNAS], show="headings", height=12)
        for clave, titulo, ancho in COLUMNAS:
            self._tabla.heading(clave, text=titulo)
            self._tabla.column(clave, width=ancho, anchor="w")
        self._tabla.grid(row=7, column=0, columnspan=4, sticky="nsew")
