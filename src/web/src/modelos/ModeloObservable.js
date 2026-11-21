// Notificación de cambios por suscripción (variante de MVC de DA-07).
// Los Modelos avisan que cambiaron a quien se haya suscripto, sin saber quién es:
// no conocen a la Vista ni a los Controladores.

/** Modelo base que avisa a sus suscriptos cada vez que cambia. */
export class ModeloObservable {
  #suscriptores = new Set()

  /** Suscribe una función a los cambios y devuelve la función que cancela la suscripción. */
  suscribir(alCambiar) {
    this.#suscriptores.add(alCambiar)
    return () => this.#suscriptores.delete(alCambiar)
  }

  /** Avisa a todos los suscriptos que el modelo cambió. */
  notificar() {
    for (const alCambiar of this.#suscriptores) alCambiar()
  }
}
