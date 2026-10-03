# Evaluación heurística — Pantalla 1: Carga de secuencia

- **Mockup inicial:** [`../mockups/pantalla-01-carga-secuencia_HU01-HU02_inicial.html`](../mockups/pantalla-01-carga-secuencia_HU01-HU02_inicial.html)
- **Mockup final:** [`../mockups/pantalla-01-carga-secuencia_HU01-HU02_final.html`](../mockups/pantalla-01-carga-secuencia_HU01-HU02_final.html)
- **HUs cubiertas:** `HU01_CU001_B`, `HU02_CU001_E1`

---

## 1. Primer ciclo (generación del HTML)

El prompt usado para la generación del HTML y el resumen de la respuesta de la IA están en [`../mockups/README.md`](../mockups/README.md). La salida del primer ciclo es el archivo `_inicial.html`.

---

## 2. Segundo ciclo — Evaluación heurística con IA

### 2.1 Prompt que le pasamos a la IA

> Actuá como especialista en interfaz de usuario. Te paso el HTML de una pantalla de nuestro proyecto LocalBlast (GUI para BLAST+), el perfil del Investigador/a y las HU que cubre la pantalla. Evaluala **heurística por heurística** según las 10 heurísticas de Nielsen, teniendo en cuenta este perfil y no un usuario genérico. Para cada heurística decime si **se cumple, se cumple parcialmente o se incumple**, y por qué. La pantalla muestra apilados cuatro estados (vacío, cargado, carácter inválido, FASTA sin cuerpo): evaluá los cuatro.

### 2.2 Respuesta de la IA

| # | Heurística | Veredicto | Fundamento (resumen) |
|---|---|---|---|
| 1 | Visibilidad del estado | parcial | El stepper y la tarjeta de "cargada" son claros, pero no hay feedback mientras se sube un archivo. |
| 2 | Mundo real | cumple | Lenguaje del dominio (FASTA, alfabeto, aa, inferido). |
| 3 | Control y libertad | parcial | "Reemplazar secuencia" no pide confirmación y la secuencia es la base de todo lo que sigue. |
| 4 | Consistencia | cumple | Botones, zona de drop y banners siguen convenciones web. |
| 5 | Prevención de errores | parcial | Validar on-blur ahorraría un ciclo al estudiante. |
| 6 | Reconocimiento | parcial | El ejemplo FASTA solo aparece como placeholder gris, se pierde al escribir. |
| 7 | Flexibilidad | parcial | No hay reutilización de últimas secuencias ni atajos para el sénior. |
| 8 | Minimalista | cumple | Paleta sobria, sin decoración. |
| 9 | Recuperación de errores | parcial | El error de carácter inválido es excelente; el de "FASTA sin cuerpo" no muestra un ejemplo del formato correcto. |
| 10 | Ayuda y documentación | incumple | No hay ningún link ni popover de ayuda sobre qué es un FASTA. |

### 2.3 Lo que la IA sugirió para los parciales / incumplidos

- H1: estado "subiendo…" para archivos grandes.
- H3: pedir confirmación antes de reemplazar.
- H5: validar on-blur apenas se pega el texto.
- H6 + H10: popover "¿qué es un FASTA?" con ejemplo siempre visible.
- H7: historial de últimas secuencias cargadas; atajo de teclado.
- H9: incluir mini-ejemplo en el banner de error de "FASTA sin cuerpo".

---
