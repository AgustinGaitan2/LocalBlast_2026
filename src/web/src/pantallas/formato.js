// Formato de los números para mostrarlos. Es presentación, no regla del negocio.

/** Formatea un E-value como lo muestra BLAST+ (0.0, 2e-130 o 0.42). */
export function formatearEvalue(evalue) {
  if (evalue === 0) return '0.0'
  if (evalue < 0.001) return evalue.toExponential(0)
  return Number(evalue.toPrecision(2)).toString()
}

/** Formatea el score con un decimal. */
export function formatearScore(score) {
  return score.toFixed(1)
}

/** Formatea un porcentaje con un decimal y el signo %. */
export function formatearPorcentaje(valor) {
  return `${valor.toFixed(1)}%`
}

/** Formatea la hora de una fecha (HH:MM:SS), o un guion si no hay fecha. */
export function formatearHora(fecha) {
  return fecha ? fecha.toLocaleTimeString('es-AR', { hour12: false }) : '—'
}

/** Formatea una duración en milisegundos como MM:SS. */
export function formatearDuracion(milisegundos) {
  const segundos = Math.max(0, Math.floor(milisegundos / 1000))
  const minutos = Math.floor(segundos / 60)
  return `${String(minutos).padStart(2, '0')}:${String(segundos % 60).padStart(2, '0')}`
}
