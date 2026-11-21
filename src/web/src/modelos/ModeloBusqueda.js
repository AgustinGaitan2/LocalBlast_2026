import { ModeloObservable } from './ModeloObservable.js'

/** Estados de la ejecución en el cliente (regla R6 del diseño detallado). */
export const Estado = Object.freeze({
  VALIDADA: 'validada',
  EN_EJECUCION: 'en_ejecucion',
  FINALIZADA: 'finalizada',
  CON_ERROR: 'con_error',
})

/** Modelo de búsqueda: guarda la configuración validada y el estado de su ejecución. */
export class ModeloBusqueda extends ModeloObservable {
  #configuracion
  #estado = Estado.VALIDADA
  #mensajeError = null
  #inicio = null
  #fin = null

  /** Crea el modelo con una búsqueda ya validada (precondición de HU08, la deja hecha HU05). */
  constructor(configuracionValidada) {
    super()
    this.#configuracion = Object.freeze(structuredClone(configuracionValidada))
  }

  /** Devuelve la configuración validada, que no se puede modificar. */
  obtener_configuracion() {
    return this.#configuracion
  }

  /** Devuelve el estado actual de la ejecución. */
  obtener_estado() {
    return this.#estado
  }

  /** Devuelve el mensaje del último error, o null si no hubo. */
  obtener_mensaje_error() {
    return this.#mensajeError
  }

  /** Devuelve el momento en que empezó la ejecución. */
  obtener_inicio() {
    return this.#inicio
  }

  /** Devuelve el momento en que terminó la ejecución, bien o con error. */
  obtener_fin() {
    return this.#fin
  }

  /** Marca la búsqueda en ejecución; solo se ejecuta una búsqueda validada o una que falló. */
  marcar_en_ejecucion() {
    if (this.#estado !== Estado.VALIDADA && this.#estado !== Estado.CON_ERROR) {
      throw new Error('La búsqueda ya se está ejecutando o ya terminó.')
    }
    this.#estado = Estado.EN_EJECUCION
    this.#mensajeError = null
    this.#inicio = new Date()
    this.#fin = null
    this.notificar()
  }

  /** Marca la búsqueda como finalizada y registra cuándo terminó. */
  marcar_finalizada() {
    this.#estado = Estado.FINALIZADA
    this.#fin = new Date()
    this.notificar()
  }

  /** Registra que la ejecución falló, con el mensaje recibido. */
  registrar_error(mensaje) {
    this.#estado = Estado.CON_ERROR
    this.#mensajeError = mensaje
    this.#fin = new Date()
    this.notificar()
  }
}
