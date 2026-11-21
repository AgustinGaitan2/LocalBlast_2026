// ModeloBusqueda, ModeloResultados y ModeloObservable (regla R6 y notificación de cambios de DA-07).
import { afterEach, describe, expect, it, vi } from 'vitest'
import { Estado, ModeloBusqueda } from '../../src/web/src/modelos/ModeloBusqueda.js'
import { ModeloResultados } from '../../src/web/src/modelos/ModeloResultados.js'
import { ModeloObservable } from '../../src/web/src/modelos/ModeloObservable.js'
import { CONFIGURACION, FILAS } from './dobles.js'

/** Crea un modelo de búsqueda llevado al estado indicado. */
function crearModeloEn(estado) {
  const modelo = new ModeloBusqueda(CONFIGURACION)
  if (estado === Estado.VALIDADA) return modelo
  modelo.marcar_en_ejecucion()
  if (estado === Estado.FINALIZADA) modelo.marcar_finalizada()
  if (estado === Estado.CON_ERROR) modelo.registrar_error('falló')
  return modelo
}

describe('ModeloBusqueda.marcar_en_ejecucion (complejidad 3)', () => {
  // CP-45 · Caja blanca, rama "validada"
  it('pasa una búsqueda validada a en ejecución y avisa a los suscriptos', () => {
    const modelo = crearModeloEn(Estado.VALIDADA)
    const alCambiar = vi.fn()
    modelo.suscribir(alCambiar)

    modelo.marcar_en_ejecucion()

    expect(modelo.obtener_estado()).toBe(Estado.EN_EJECUCION)
    expect(alCambiar).toHaveBeenCalledOnce()
  })

  // CP-46 · Caja blanca, rama "con error": se puede reintentar y se limpia el error anterior
  it('permite reintentar una búsqueda que terminó con error', () => {
    const modelo = crearModeloEn(Estado.CON_ERROR)

    modelo.marcar_en_ejecucion()

    expect(modelo.obtener_estado()).toBe(Estado.EN_EJECUCION)
    expect(modelo.obtener_mensaje_error()).toBeNull()
  })

  // CP-47 · Caja blanca, rama de rechazo: ni en ejecución ni finalizada se vuelve a ejecutar
  it.each([Estado.EN_EJECUCION, Estado.FINALIZADA])('rechaza ejecutar una búsqueda %s', (estado) => {
    const modelo = crearModeloEn(estado)

    expect(() => modelo.marcar_en_ejecucion()).toThrow('ya se está ejecutando o ya terminó')
    expect(modelo.obtener_estado()).toBe(estado)
  })
})

describe('ModeloBusqueda', () => {
  // CP-57 · Caja negra · precondición de HU08: la configuración validada no se puede alterar desde afuera
  it('conserva una copia inmutable de la configuración validada', () => {
    const original = structuredClone(CONFIGURACION)
    const modelo = new ModeloBusqueda(original)
    original.base_datos = 'otra'

    expect(modelo.obtener_configuracion().base_datos).toBe(CONFIGURACION.base_datos)
    expect(Object.isFrozen(modelo.obtener_configuracion())).toBe(true)
  })
})

describe('ModeloBusqueda: momento de fin', () => {
  afterEach(() => vi.useRealTimers())

  // CP-58 · Caja negra · CA-03 (agregada al ver el reporte de cobertura): la hora que muestra
  // el chip "Guardado en el historial" es la del momento en que terminó la ejecución.
  it.each([
    ['finaliza', (modelo) => modelo.marcar_finalizada()],
    ['termina con error', (modelo) => modelo.registrar_error('falló')],
  ])('registra la hora de fin cuando la búsqueda %s', (_, terminar) => {
    vi.useFakeTimers()
    vi.setSystemTime(new Date('2026-11-21T15:30:00Z'))
    const modelo = crearModeloEn(Estado.VALIDADA)
    modelo.marcar_en_ejecucion()
    vi.setSystemTime(new Date('2026-11-21T15:30:04Z'))

    terminar(modelo)

    expect(modelo.obtener_fin()).toEqual(new Date('2026-11-21T15:30:04Z'))
  })
})

describe('ModeloResultados.cargar', () => {
  // CP-54 · Caja negra · CA-02: guarda las filas tal como llegaron y avisa del cambio
  it('guarda las filas recibidas y avisa a los suscriptos', () => {
    const modelo = new ModeloResultados()
    const alCambiar = vi.fn()
    modelo.suscribir(alCambiar)

    modelo.cargar(FILAS)

    expect(modelo.obtener_filas()).toEqual(FILAS)
    expect(modelo.estan_cargados()).toBe(true)
    expect(alCambiar).toHaveBeenCalledOnce()
  })
})

describe('ModeloObservable.notificar (complejidad 2)', () => {
  // CP-53 · Caja blanca, ciclo de suscriptores: avisa a todos y deja de avisar al que se desuscribió
  it('avisa a cada suscripto y no al que canceló su suscripción', () => {
    const observable = new ModeloObservable()
    const primero = vi.fn()
    const segundo = vi.fn()
    const cancelar = observable.suscribir(primero)
    observable.suscribir(segundo)

    cancelar()
    observable.notificar()

    expect(primero).not.toHaveBeenCalled()
    expect(segundo).toHaveBeenCalledOnce()
  })
})
