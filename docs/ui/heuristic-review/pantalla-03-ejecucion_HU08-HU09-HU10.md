# Evaluación heurística — Pantalla 3: Ejecución en progreso

- **Mockup inicial:** [`../mockups/pantalla-03-ejecucion_HU08-HU09-HU10_inicial.html`](../mockups/pantalla-03-ejecucion_HU08-HU09-HU10_inicial.html)
- **Mockup final:** [`../mockups/pantalla-03-ejecucion_HU08-HU09-HU10_final.html`](../mockups/pantalla-03-ejecucion_HU08-HU09-HU10_final.html)
- **HUs cubiertas:** `HU08_CU004_B`, `HU09_CU004_A1`, `HU10_CU004_E1`

---

## 1. Primer ciclo (generación del HTML)

Prompt y resumen de la generación: ver [`../mockups/README.md`](../mockups/README.md). La salida es `_inicial.html`.

---

## 2. Segundo ciclo — Evaluación heurística con IA

### 2.1 Prompt que le pasamos a la IA

> Actuá como especialista en interfaz de usuario. Te paso el HTML de la pantalla de **ejecución** de LocalBlast, el perfil del Investigador/a y las 3 HU cubiertas. Evaluala **heurística por heurística** según las 10 heurísticas de Nielsen, con este perfil concreto. Para cada una: **cumple / parcial / incumple**, por qué, y una mejora si corresponde. La pantalla muestra 4 estados apilados: ejecución en curso, cancelación, timeout de NCBI, rechazo explícito de NCBI. Evaluá los cuatro.

### 2.2 Respuesta de la IA

| # | Heurística | Veredicto | Fundamento (resumen) |
|---|---|---|---|
| 1 | Visibilidad del estado | cumple | Barra de progreso, tiempo, metadatos, spinner, y chip "corriendo" en la barra lateral. |
| 2 | Mundo real | cumple | "Ejecutando `blastp` contra `nr` (NCBI remoto)" + bloque `[BLAST+ stderr]` para los errores. |
| 3 | Control y libertad | cumple | Botón "Cancelar" visible y hint "podés seguir trabajando". |
| 4 | Consistencia | cumple | Componentes y paleta coherentes con el resto. |
| 5 | Prevención de errores | parcial | "Cancelar búsqueda" no pide confirmación. Un click accidental tira varios minutos. |
| 6 | Reconocimiento | cumple | Toda la config que llevó a esta ejecución está visible arriba. |
| 7 | Flexibilidad | cumple | Barra lateral permite navegar sin interrumpir la ejecución. |
| 8 | Minimalista | cumple | Es la pantalla menos cargada del flujo. |
| 9 | Recuperación de errores | cumple | Mensajes distinguen timeout de rechazo, muestran stderr literal, ofrecen "Reintentar". |
| 10 | Ayuda y documentación | parcial | Nada que aclare qué pasa si se cierra la pestaña durante la ejecución. |

### 2.3 Lo que la IA sugirió para los parciales

- H5: confirmación de dos pasos antes de cancelar.
- H9 (observación suelta dentro del "cumple"): mostrar la garantía de "no se guardó nada" **antes** de cancelar, no solo después.
- H10: línea sobre qué pasa si se cierra la ventana.

---

## 3. Revisión del grupo

| Hallazgo | Decisión | Por qué |
|---|---|---|
| H5 — confirmar cancelación | **aceptado** | Mismo criterio que las pantallas anteriores: acción destructiva pide confirmación. Entra al ajuste. |
| H9 (refuerzo) — "no se guardó" durante la ejecución | **aceptado** | Lo tomamos del comentario de la IA dentro de H9 y lo levantamos como hallazgo propio. HU11 CA-02 dice que la persistencia es al final. Si el investigador no sabe eso, duda en cancelar. Entra al ajuste. |
| H10 — qué pasa si cierro la pestaña | **rechazado** | El comportamiento concreto depende de la implementación, no está definido en TP1. Prometerlo en el maquetado y después no cumplirlo es peor que no decir nada. |

**Cambios que entran al ciclo adicional:** chip "aún no persistida en el historial" durante la ejecución; bloque de confirmación antes de cancelar.

---
