import { useEffect, useReducer } from 'react'

/** Suscribe la Vista a un Modelo para volver a dibujarla cada vez que cambia (solo lectura). */
export function useObservar(modelo) {
  const [, redibujar] = useReducer((version) => version + 1, 0)
  useEffect(() => modelo.suscribir(redibujar), [modelo])
}
