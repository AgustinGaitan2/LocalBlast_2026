import { ModeloObservable } from './ModeloObservable.js'

/**
 * Modelo de resultados: guarda las filas crudas que devolvió el Backend para la tabla.
 * En HU11 se le agregan los filtros post-búsqueda, que siempre se calculan desde este crudo.
 */
export class ModeloResultados extends ModeloObservable {
  #filas = []
  #cargados = false

  /** Carga las filas recibidas como una copia que no se puede modificar. */
  cargar(filas) {
    this.#filas = Object.freeze(filas.map((fila) => Object.freeze({ ...fila })))
    this.#cargados = true
    this.notificar()
  }

  /** Devuelve las filas cargadas. */
  obtener_filas() {
    return this.#filas
  }

  /** Indica si ya se cargaron resultados. */
  estan_cargados() {
    return this.#cargados
  }
}
