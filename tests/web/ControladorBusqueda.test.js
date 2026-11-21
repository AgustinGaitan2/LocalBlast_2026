// ControladorBusqueda: Secuencias 1 y 2 del lado de la Aplicación Web (CA-01, CA-02, R4, R6).
import { describe, expect, it } from 'vitest'
import { ErrorBlast } from '../../src/web/src/cliente/ClienteBackend.js'
import { ControladorBusqueda } from '../../src/web/src/controladores/ControladorBusqueda.js'
import { Estado, ModeloBusqueda } from '../../src/web/src/modelos/ModeloBusqueda.js'
import { ModeloResultados } from '../../src/web/src/modelos/ModeloResultados.js'
import { CONFIGURACION, ClienteDoble, FILAS } from './dobles.js'

/** Arma el controlador con modelos nuevos y un cliente doble. */
function armarControlador() {
  const modeloBusqueda = new ModeloBusqueda(CONFIGURACION)
  const modeloResultados = new ModeloResultados()
  const cliente = new ClienteDoble()
  const controlador = new ControladorBusqueda(modeloBusqueda, modeloResultados, cliente)
  return { modeloBusqueda, modeloResultados, cliente, controlador }
}

describe('ControladorBusqueda.ejecutar', () => {
  // CP-01 · Caja negra · CA-01: la ejecución no bloquea; mientras el Backend no responde,
  // la búsqueda figura en ejecución y la interfaz puede seguir mostrando y navegando.
  it('marca la búsqueda en ejecución y no espera la respuesta para devolver el control', async () => {
    const { modeloBusqueda, modeloResultados, cliente, controlador } = armarControlador()

    const ejecucion = controlador.ejecutar() // no se espera: el Backend todavía no respondió

    expect(modeloBusqueda.obtener_estado()).toBe(Estado.EN_EJECUCION)
    expect(modeloBusqueda.obtener_inicio()).toBeInstanceOf(Date)
    expect(modeloResultados.estan_cargados()).toBe(false)
    expect(cliente.recibido).toEqual([CONFIGURACION])
    cliente.responder(FILAS)
    await ejecucion
  })

  // CP-07 · Caja negra · CA-02 (y camino "sin error" de la caja blanca): al terminar, la tabla queda cargada
  it('al recibir las filas las carga en el modelo de resultados y finaliza la búsqueda', async () => {
    const { modeloBusqueda, modeloResultados, cliente, controlador } = armarControlador()

    const ejecucion = controlador.ejecutar()
    cliente.responder(FILAS)
    await ejecucion

    expect(modeloResultados.obtener_filas()).toEqual(FILAS)
    expect(modeloBusqueda.obtener_estado()).toBe(Estado.FINALIZADA)
  })

  // CP-14 · Caja negra · R4 (y camino "con error" de la caja blanca): sin tabla y con el mensaje literal
  it('si BLAST+ falla registra su mensaje literal y no carga resultados', async () => {
    const { modeloBusqueda, modeloResultados, cliente, controlador } = armarControlador()
    const mensaje = 'BLAST Database error: No alias or index file found'

    const ejecucion = controlador.ejecutar()
    cliente.fallar(new ErrorBlast(mensaje))
    await ejecucion

    expect(modeloBusqueda.obtener_estado()).toBe(Estado.CON_ERROR)
    expect(modeloBusqueda.obtener_mensaje_error()).toBe(mensaje)
    expect(modeloResultados.estan_cargados()).toBe(false)
  })

  // CP-02 · Caja negra · CA-01: una búsqueda en ejecución no se puede lanzar dos veces
  it('no permite ejecutar de nuevo mientras la búsqueda está en ejecución', async () => {
    const { cliente, controlador } = armarControlador()

    const primera = controlador.ejecutar()

    await expect(controlador.ejecutar()).rejects.toThrow('ya se está ejecutando')
    expect(cliente.recibido).toHaveLength(1)
    cliente.responder(FILAS)
    await primera
  })
})
