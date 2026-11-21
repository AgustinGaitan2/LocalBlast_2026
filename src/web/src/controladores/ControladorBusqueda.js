// Sigue las Secuencias 1 y 2 del diseño detallado. Cambia los Modelos; la Vista se
// entera del cambio porque los observa (DA-07), no porque el Controlador la llame.

/** Controlador de búsqueda: interpreta la acción "ejecutar" del investigador. */
export class ControladorBusqueda {
  #modeloBusqueda
  #modeloResultados
  #cliente

  /** Recibe los dos Modelos y el Cliente del Backend con los que trabaja. */
  constructor(modeloBusqueda, modeloResultados, cliente) {
    this.#modeloBusqueda = modeloBusqueda
    this.#modeloResultados = modeloResultados
    this.#cliente = cliente
  }

  /** Ejecuta la búsqueda validada sin bloquear la interfaz y carga el resultado o el error (CA-01). */
  async ejecutar() {
    const configuracion = this.#modeloBusqueda.obtener_configuracion()
    this.#modeloBusqueda.marcar_en_ejecucion()
    try {
      const filas = await this.#cliente.ejecutar_busqueda(configuracion)
      this.#modeloResultados.cargar(filas)
      this.#modeloBusqueda.marcar_finalizada()
    } catch (error) {
      this.#modeloBusqueda.registrar_error(error.message)
    }
  }
}
