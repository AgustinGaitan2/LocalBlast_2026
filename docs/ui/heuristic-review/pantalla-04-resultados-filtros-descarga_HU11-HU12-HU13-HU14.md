# Evaluación heurística — Pantalla 4: Resultados, filtros y descarga

- **Mockup inicial:** [`../mockups/pantalla-04-resultados-filtros-descarga_HU11-HU12-HU13-HU14_inicial.html`](../mockups/pantalla-04-resultados-filtros-descarga_HU11-HU12-HU13-HU14_inicial.html)
- **Mockup final:** [`../mockups/pantalla-04-resultados-filtros-descarga_HU11-HU12-HU13-HU14_final.html`](../mockups/pantalla-04-resultados-filtros-descarga_HU11-HU12-HU13-HU14_final.html)
- **HUs cubiertas:** `HU11_CU005_B`, `HU12_CU006_B`, `HU13_CU007_B`, `HU14_CU007_A1`

---

## 1. Primer ciclo (generación del HTML)

Prompt y resumen de la generación: ver [`../mockups/README.md`](../mockups/README.md). La salida es `_inicial.html`.

---

## 2. Segundo ciclo — Evaluación heurística con IA

### 2.1 Prompt que le pasamos a la IA

> Actuá como especialista en interfaz de usuario. Te paso el HTML de la pantalla de **resultados, filtros y descarga** de LocalBlast, el perfil del Investigador/a y las 4 HU cubiertas. Evaluala **heurística por heurística** según las 10 heurísticas de Nielsen, con este perfil concreto. Para cada una: **cumple / parcial / incumple**, por qué, y una mejora si corresponde. La pantalla muestra 2 estados apilados: tabla filtrada con 12/54 hits visibles, y tabla vacía por filtros estrictos. Evaluá los dos.

### 2.2 Respuesta de la IA

| # | Heurística | Veredicto | Fundamento (resumen) |
|---|---|---|---|
| 1 | Visibilidad del estado | cumple | "12 de 54", badge de filtros activos, chip "Guardado en el historial", botón "Descargar N visibles" dinámico. |
| 2 | Mundo real | cumple | Columnas y filtros con los nombres esperados; formatos con nombres del dominio. |
| 3 | Control y libertad | parcial | "Limpiar filtros" es un link subrayado chico, poco visible. |
| 4 | Consistencia | cumple | Panel lateral + tabla + radios + botón primario. Componentes esperables. |
| 5 | Prevención de errores | parcial | El input de E-value es texto libre sin validación visible. |
| 6 | Reconocimiento | parcial | Columnas y formatos tienen nombre pero no definición. |
| 7 | Flexibilidad | cumple | Cinco formatos, sliders rápidos, descarga con metadatos. |
| 8 | Minimalista | parcial | Las mini-barras junto a los porcentajes podrían competir con el número. (La IA aclara: en pantalla ayudan, en papel se ven cargadas.) |
| 9 | Recuperación de errores | parcial | El banner de tabla vacía informa, pero no da un click para salir del estado. |
| 10 | Ayuda y documentación | incumple | Sin tooltips ni ayuda contextual para formatos y columnas. |

### 2.3 Lo que la IA sugirió para los parciales / incumplidos

- H3: "Limpiar filtros" como botón real con jerarquía propia.
- H5: validación del input de E-value.
- H6 + H10: tooltips en columnas de la tabla y en los formatos de descarga.
- H9: botones de sugerencia accionables en el estado vacío.

---
