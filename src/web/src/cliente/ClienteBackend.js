// Cliente del Backend: lo único de la Aplicación Web que conoce la interfaz REST.

/** Error de BLAST+; su mensaje es el literal de BLAST+, sin reinterpretar. */
export class ErrorBlast extends Error {
  /** Crea el error con el mensaje que informó BLAST+. */
  constructor(mensaje) {
    super(mensaje)
    this.name = 'ErrorBlast'
  }
}

/** Cliente que envía las solicitudes de ejecución al Backend por HTTP. */
export class ClienteBackend {
  #urlBase

  /** Crea el cliente; por defecto usa el mismo origen que la página. */
  constructor(urlBase = '') {
    this.#urlBase = urlBase
  }

  /** Pide la ejecución y devuelve las filas; lanza ErrorBlast, o Error si falla la comunicación. */
  async ejecutar_busqueda(configuracion) {
    let respuesta
    try {
      respuesta = await fetch(`${this.#urlBase}/api/busquedas/ejecucion`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(configuracion),
      })
    } catch {
      throw new Error(
        'No se pudo conectar con el servidor de LocalBlast. Verificá que el Backend esté en ejecución.',
      )
    }
    const cuerpo = await respuesta.json().catch(() => null)
    if (respuesta.ok) return cuerpo.filas
    if (cuerpo?.tipo === 'ErrorBlast') throw new ErrorBlast(cuerpo.mensaje)
    throw new Error(`El servidor rechazó la solicitud (HTTP ${respuesta.status}).`)
  }
}
