# Maquetado HTML — Primer ciclo de generación con IA

Esta carpeta contiene el maquetado HTML del flujo de navegación del Investigador/a, generado en el **primer ciclo** del proceso de maquetado asistido por IA. Cada archivo corresponde a una de las pantallas definidas en el flujo de navegación del perfil ([`../user-profiles/investigador.md`](../user-profiles/investigador.md), sección 3) y lleva en el nombre las historias de usuario que respalda.

## Archivos

| Archivo | Pantalla del flujo | HUs cubiertas |
|---|---|---|
| [`pantalla-01-carga-secuencia_HU01-HU02.html`](pantalla-01-carga-secuencia_HU01-HU02.html) | Nueva búsqueda — Secuencia query | `HU01_CU001_B`, `HU02_CU001_E1` |
| [`pantalla-02-configuracion-validacion_HU03-HU04-HU05-HU06-HU07.html`](pantalla-02-configuracion-validacion_HU03-HU04-HU05-HU06-HU07.html) | Nueva búsqueda — Configuración + validación | `HU03_CU002_B`, `HU04_CU002_A1`, `HU05_CU003_B`, `HU06_CU003_E1`, `HU07_CU003_E2` |
| [`pantalla-03-ejecucion_HU08-HU09-HU10.html`](pantalla-03-ejecucion_HU08-HU09-HU10.html) | Ejecución en progreso | `HU08_CU004_B`, `HU09_CU004_A1`, `HU10_CU004_E1` |
| [`pantalla-04-resultados-filtros-descarga_HU11-HU12-HU13-HU14.html`](pantalla-04-resultados-filtros-descarga_HU11-HU12-HU13-HU14.html) | Resultados · filtros · descarga | `HU11_CU005_B`, `HU12_CU006_B`, `HU13_CU007_B`, `HU14_CU007_A1` |

Las **14 HUs del catálogo** del TP1 que requieren interfaz quedan cubiertas por estos cuatro archivos. La pantalla de autenticación mencionada en el flujo del perfil **no se maqueta** en esta iteración: no hay HU que la respalde y el principio de diseño del grupo es *"si una pantalla no está respaldada por alguna HU, no se maqueta"*. El resto del flujo asume sesión ya iniciada.

Cada archivo HTML muestra apilados el **estado primario** (camino feliz) y los **estados alternativos y de excepción** cubiertos por sus HUs, cada uno con una etiqueta visible que indica a qué HU y a qué criterio de aceptación corresponde. Esta decisión se tomó para que la evaluación visual pueda recorrer todos los estados sin necesidad de interactuar. En la implementación final solo un estado será visible al mismo tiempo.

---

## 1. Criterios definidos por el grupo antes de pedir a la IA

Antes de redactar el prompt, el grupo acordó los siguientes criterios para evitar que la IA eligiera por su cuenta decisiones que son de dominio del proyecto:

### 1.1 Tipo de sistema

- **Aplicación web** (SRS 1.3 fija *"Interfaz web"* en el alcance), específicamente una GUI para BLAST+.
- **Pensada para desktop/laptop** con navegador moderno; el perfil del Investigador/a lo marca explícitamente (*"el sistema no está pensado para uso cómodo en celular"* — [`investigador.md`](../user-profiles/investigador.md) 1.3). El maquetado se diseña para anchos típicos de desktop.

### 1.2 Lenguaje y framework del maquetado

- **HTML + CSS puro**, sin framework. Un archivo `.html` autocontenido por pantalla, con el CSS en una etiqueta `<style>` embebida, para que cada archivo se abra en cualquier navegador sin build-step.
- **Sin JavaScript** (ni interactividad real): el objetivo del primer ciclo es la maqueta de interfaz, no el prototipo funcional. Los distintos estados por HU se renderizan apilados en el mismo archivo con etiquetas visibles, en vez de intercambiarse por script.

### 1.3 Perfil de usuario y escenario de uso

- **Único actor con historias de usuario:** Investigador/a (ver [`investigador.md`](../user-profiles/investigador.md)).
- **Escenario de uso de referencia:** camino feliz construido alrededor que cierra el ciclo completo de valor y encadena naturalmente las HUs necesarias.
- **Variantes realistas** que el maquetado debe sostener: secuencia inválida y base local no disponible, además de los demás caminos de excepción (`HU06`, `HU07`, `HU09`, `HU10`, `HU14`).

### 1.4 Otros criterios relevantes para este proyecto

- **Rango de nivel técnico del usuario.** El perfil del Investigador cubre desde estudiante de grado hasta investigador sénior. La interfaz debe ser accesible para el extremo inferior (defaults sensatos, mensajes de error diagnósticos) **sin** sacarle control al extremo superior (poder ajustar parámetros, elegir bases locales, descargar en formatos como BLAST XML o tabular `-outfmt 6`).
- **Defaults por programa.** Los valores por defecto de los parámetros pre-búsqueda deben verse como *"recalculados según el programa BLAST elegido"* (RF-06): el maquetado tiene que mostrar explícitamente ese comportamiento, no fijar un único juego de números.
- **Mensajes diagnósticos, no genéricos.** Los estados de excepción deben mostrar el campo exacto en problema y, cuando corresponde, el mensaje literal de BLAST+ (`HU10`) sin reinterpretarlo. Esto está en el perfil (sección "Limitaciones y frustraciones").
- **Separación entre conjunto crudo y vista filtrada.** En la pantalla de resultados tiene que ser visible que los filtros se aplican sobre el conjunto crudo (no sobre el resultado anterior), que la descarga toma los visibles, y que el historial (D2) nunca se modifica por filtros ni por descarga. Es la base del escenario de calidad de Operabilidad y de la lógica de `HU12`/`HU13`/`HU14`.
- **Columnas mínimas de la tabla de resultados.** Según `HU11_CU005_B` CA-01: identificador del hit, score, E-value observado, % de identidad, % de cobertura. El maquetado debe mostrar al menos esas columnas (puede sumar descripción del hit como ayuda visual, pero no reemplazarlas).
- **Trazabilidad explícita HU ↔ pantalla.** El nombre de archivo debe incluir el identificador de la pantalla y las HUs cubiertas (ej.: `pantalla-01-carga-secuencia_HU01-HU02.html`), para que la correspondencia con el catálogo de HU sea verificable a simple vista.

---
