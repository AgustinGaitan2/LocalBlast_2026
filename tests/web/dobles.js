// Datos y dobles compartidos por las pruebas de la Aplicación Web.

export const CONFIGURACION = Object.freeze({
  secuencia: '>q\nMKT',
  variante: 'blastp',
  modo: 'local',
  base_datos: 'datos/blastdb/proteinas_demo',
  parametros: { evalue: 10 },
})

export const FILAS = Object.freeze([
  { id_hit: 'h1', descripcion: 'uno', score: 887.1, evalue: 0, porcentaje_identidad: 99.8, porcentaje_cobertura: 100 },
  { id_hit: 'h2', descripcion: 'dos', score: 120.4, evalue: 3e-50, porcentaje_identidad: 45.2, porcentaje_cobertura: 80 },
])

/** Doble de ClienteBackend cuya respuesta la decide la prueba (resolver o rechazar a mano). */
export class ClienteDoble {
  /** Prepara una promesa pendiente que la prueba resuelve o rechaza. */
  constructor() {
    this.recibido = []
    this.promesa = new Promise((resolver, rechazar) => {
      this.responder = resolver
      this.fallar = rechazar
    })
  }

  /** Registra la configuración recibida y devuelve la promesa pendiente. */
  ejecutar_busqueda(configuracion) {
    this.recibido.push(configuracion)
    return this.promesa
  }
}
