// ClienteBackend.ejecutar_busqueda (complejidad 5): una prueba por camino. La red se reemplaza por un doble de fetch.
import { afterEach, describe, expect, it, vi } from 'vitest'
import { ClienteBackend, ErrorBlast } from '../../src/web/src/cliente/ClienteBackend.js'
import { CONFIGURACION, FILAS } from './dobles.js'

/** Crea una respuesta HTTP simulada, con o sin cuerpo JSON. */
function crearRespuesta(status, cuerpo) {
  return {
    ok: status >= 200 && status < 300,
    status,
    json: cuerpo === undefined ? () => Promise.reject(new SyntaxError('sin JSON')) : () => Promise.resolve(cuerpo),
  }
}

/** Reemplaza fetch por un doble con la implementación indicada. */
function simularFetch(implementacion) {
  const fetchDoble = vi.fn(implementacion)
  vi.stubGlobal('fetch', fetchDoble)
  return fetchDoble
}

afterEach(() => vi.unstubAllGlobals())

describe('ClienteBackend.ejecutar_busqueda', () => {
  // CP-49 · Caja blanca, camino "respuesta correcta": envía la configuración y devuelve las filas
  it('envía la configuración por POST en JSON y devuelve las filas', async () => {
    const fetchDoble = simularFetch(async () => crearRespuesta(200, { filas: FILAS }))

    const filas = await new ClienteBackend().ejecutar_busqueda(CONFIGURACION)

    expect(filas).toEqual(FILAS)
    const [url, opciones] = fetchDoble.mock.calls[0]
    expect(url).toBe('/api/busquedas/ejecucion')
    expect(opciones.method).toBe('POST')
    expect(JSON.parse(opciones.body)).toEqual(CONFIGURACION)
  })

  // CP-50 · Caja blanca, camino "error de BLAST+": lanza ErrorBlast con el mensaje literal
  it('convierte la respuesta de error de BLAST+ en ErrorBlast', async () => {
    simularFetch(async () => crearRespuesta(502, { tipo: 'ErrorBlast', mensaje: 'BLAST Database error: x' }))

    const promesa = new ClienteBackend().ejecutar_busqueda(CONFIGURACION)

    await expect(promesa).rejects.toBeInstanceOf(ErrorBlast)
    await expect(promesa).rejects.toThrow('BLAST Database error: x')
  })

  // CP-48 · Caja blanca, camino "no hay conexión con el servidor"
  it('informa que no se pudo conectar si el servidor no responde', async () => {
    simularFetch(async () => {
      throw new TypeError('Failed to fetch')
    })

    await expect(new ClienteBackend().ejecutar_busqueda(CONFIGURACION)).rejects.toThrow(
      'No se pudo conectar con el servidor',
    )
  })

  // CP-51 · Caja blanca, camino "otro error con cuerpo JSON" (por ejemplo, solicitud mal formada)
  it('informa el código HTTP de un rechazo que no es de BLAST+', async () => {
    simularFetch(async () => crearRespuesta(422, { detail: [{ msg: 'variante inválida' }] }))

    const promesa = new ClienteBackend().ejecutar_busqueda(CONFIGURACION)

    await expect(promesa).rejects.not.toBeInstanceOf(ErrorBlast)
    await expect(promesa).rejects.toThrow('HTTP 422')
  })

  // CP-52 · Caja blanca, camino "otro error sin cuerpo JSON"
  it('informa el código HTTP aunque la respuesta no traiga JSON', async () => {
    simularFetch(async () => crearRespuesta(500))

    await expect(new ClienteBackend().ejecutar_busqueda(CONFIGURACION)).rejects.toThrow('HTTP 500')
  })
})
