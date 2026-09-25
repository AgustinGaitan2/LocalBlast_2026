# Historias de Usuario — LocalBlast

Cada historia de usuario detalla **un slice puntual** de un caso de uso (relación 1:1). El identificador de la HU conserva explícitamente el del slice de origen, para que la trazabilidad sea directa: la HU llamada `HU01_CU001_B` detalla el slice básico `B` del caso de uso `CU001`; la HU `HU13_CU007_B` detalla el (único) slice básico `B` del caso de uso `CU007`.

Formato de cada HU:

- **Deriva de**: qué CU y qué slice detalla.
- **Realiza**: qué RF materializa este slice (heredados del CU y del slice de origen).
- **Rol – meta – motivo**: "Como … quiero … para …".
- **Criterios de aceptación**: en formato **Given-When-Then**, trazables a la precondición y postcondición del slice.

Para el TP1 se detallan las HU de **todos los slices identificados en los casos de uso** — los siete básicos (`CU001_B`, `CU002_B`, `CU003_B`, `CU004_B`, `CU005_B`, `CU006_B`, `CU007_B`), las tres alternativas (`CU002_A1`, `CU004_A1`, `CU007_A1`) y las cuatro excepciones (`CU001_E1`, `CU003_E1`, `CU003_E2`, `CU004_E1`). En total, 14 historias de usuario.

**Numeración:** las HU se enumeran de forma consecutiva por CU y, dentro de cada CU, en el orden: slice básico (`B`) → slices alternativos (`A1`, `A2`, …) → slices de excepción (`E1`, `E2`, …). Así los identificadores acompañan el orden en el que aparecen los slices en [`casos-de-uso.md`](casos-de-uso.md).

---

## HU derivadas de CU001 · Cargar la secuencia query

### HU01_CU001_B · Cargar la secuencia query y chequear su formato

- **Deriva de:** `CU001`, slice `B` (pasos 1-2 del camino feliz)
- **Realiza:** RF-01, RF-02

> **Como** investigador/a,
> **quiero** subir un archivo FASTA o pegar la secuencia como texto y que el sistema la deje disponible con su alfabeto inferido,
> **para** poder reutilizar la misma secuencia en distintas configuraciones de búsqueda sin tener que cargarla de nuevo.

**Criterios de aceptación (Given-When-Then)**

- **CA-01.** Carga de secuencia FASTA de proteína desde archivo:
  - **Given** un archivo `.fasta` bien formado con un único registro de secuencia de aminoácidos válidos,
  - **When** el investigador lo sube desde el formulario,
  - **Then** el sistema deja la secuencia disponible en la sesión, muestra el alfabeto inferido "proteína" y habilita los controles del `CU002` para configurar la búsqueda.

- **CA-02.** Carga de secuencia pegada como texto plano:
  - **Given** una secuencia de ADN pegada en el textarea del formulario, sin encabezado FASTA,
  - **When** el investigador confirma la carga,
  - **Then** el sistema la acepta como secuencia plana, infiere alfabeto "ADN" y la deja disponible para `CU002`.

- **CA-03.** Reutilización de la secuencia cargada:
  - **Given** una secuencia ya cargada en la sesión con la que el investigador ya lanzó una búsqueda,
  - **When** el investigador vuelve al formulario para armar otra configuración distinta,
  - **Then** la secuencia sigue disponible sin necesidad de volver a cargarla, y solo se reinicia el resto del formulario.

---

## HU derivadas de CU002 · Refinar los resultados con filtros post-búsqueda

### HU09_CU002_B · Refinar la vista con filtros post-búsqueda

- **Deriva de:** `CU002`, slice `B` (único slice básico; el camino feliz no se subdivide)
- **Realiza:** RF-09

> **Como** investigador/a,
> **quiero** aplicar filtros post-búsqueda sobre la tabla de resultados y verla refrescada en el momento, sin correr BLAST otra vez,
> **para** poder explorar interactivamente los alineamientos con distintos criterios y quedarme mirando el subconjunto relevante, aunque no llegue a descargar nada.

**Criterios de aceptación (Given-When-Then)**

- **CA-01.** Filtrado interactivo sin re-ejecución de BLAST:
  - **Given** una tabla de resultados con al menos 20 alineamientos y filtros post-búsqueda establecidos en identidad ≥ 80% y cobertura ≥ 50%,
  - **When** el investigador confirma los filtros,
  - **Then** la tabla se re-filtra en el momento mostrando solo los hits que cumplen ambos umbrales, sin volver a invocar a BLAST+.

- **CA-02.** Ajuste sucesivo de filtros no re-ejecuta BLAST:
  - **Given** una tabla ya filtrada por identidad ≥ 80%,
  - **When** el investigador afloja el umbral a identidad ≥ 60% y agrega cobertura ≥ 70%,
  - **Then** la tabla se re-filtra sobre el conjunto crudo original (no sobre el resultado del filtro anterior) y aparecen los hits que cumplen los nuevos umbrales, sin ninguna invocación adicional a BLAST+.

- **CA-03.** Filtros no modifican el historial:
  - **Given** una búsqueda ya persistida en D2 al terminar su ejecución (postcondición de `CU001_B2`),
  - **When** el investigador aplica cualquier combinación de filtros post-búsqueda,
  - **Then** la entrada en D2 no se modifica: sigue conteniendo el conjunto **crudo** completo de resultados, para que en el futuro se pueda volver a esa búsqueda y probar filtros distintos.

---

## HU derivadas de CU003 · Descargar los resultados en un formato

### HU10_CU003_B · Descargar los alineamientos actualmente visibles en un formato

- **Deriva de:** `CU003`, slice `B` (único slice básico; el camino feliz no se subdivide)
- **Realiza:** RF-10

> **Como** investigador/a,
> **quiero** descargar los alineamientos que estoy viendo en la tabla —filtrados o no— en el formato que necesite,
> **para** llevarme el archivo tal cual quedó configurada la vista y seguir procesándolo por fuera del sistema.

**Criterios de aceptación (Given-When-Then)**

- **CA-01.** Descarga en el formato elegido, sobre resultados sin filtrar:
  - **Given** una tabla de resultados sin filtros post-búsqueda aplicados (postcondición directa de `CU001_B2`),
  - **When** el investigador selecciona formato "CSV" y presiona "Descargar",
  - **Then** el sistema entrega un archivo `.csv` con la totalidad de los alineamientos crudos, con una fila de encabezados que incluye al menos las columnas mínimas (identificador, score, E-value observado, % identidad, % cobertura), y una sección de metadatos con los parámetros pre-búsqueda, la base de datos y el timestamp.

- **CA-02.** Descarga en el formato elegido, sobre resultados filtrados:
  - **Given** una tabla de resultados con filtros post-búsqueda aplicados (postcondición de `CU002_B`),
  - **When** el investigador selecciona formato "CSV" y presiona "Descargar",
  - **Then** el sistema entrega un archivo `.csv` que contiene únicamente los hits que superan los filtros vigentes al momento de la descarga, con la fila de encabezados y la sección de metadatos donde figuran también los filtros post-búsqueda aplicados.

- **CA-03.** La descarga no modifica el historial:
  - **Given** una búsqueda ya persistida en D2 (postcondición de `CU001_B2`),
  - **When** el investigador descarga los resultados (con o sin filtros aplicados),
  - **Then** la entrada en D2 no se modifica ni se duplica: sigue conteniendo el conjunto crudo de resultados original, con el timestamp de la ejecución (no el de la descarga).

---

### HU11_CU003_A1 · Descarga cuando ningún resultado supera los filtros

- **Deriva de:** `CU003`, slice `A1` (camino alternativo dentro del slice `B`)
- **Realiza:** RF-10

> **Como** investigador/a,
> **quiero** poder descargar el archivo aunque los filtros post-búsqueda dejen la tabla vacía,
> **para** tener constancia del intento y de los criterios que apliqué, aun cuando ningún hit los haya superado.

**Criterios de aceptación (Given-When-Then)**

- **CA-01.** Descarga con tabla vacía:
  - **Given** una tabla de resultados con filtros post-búsqueda que dejan cero hits visibles (por ejemplo identidad ≥ 99% sobre una búsqueda de similitud lejana),
  - **When** el investigador selecciona formato "CSV" y presiona "Descargar",
  - **Then** el sistema entrega un archivo `.csv` con la fila de encabezados y una sección de metadatos de la búsqueda (parámetros pre-búsqueda, base de datos, timestamp, filtros post-búsqueda aplicados), pero **sin** filas de hits.

- **CA-02.** El historial mantiene los resultados crudos aunque la descarga sea vacía:
  - **Given** una búsqueda cuya descarga se hizo con filtros que dejaron cero hits visibles,
  - **When** el sistema termina de entregar el archivo,
  - **Then** la entrada en D2 permanece igual que antes: contiene el conjunto **completo** de resultados crudos que devolvió BLAST+ (persistido en `CU001_B2`), no la lista vacía que quedó tras el filtro, de forma que el investigador pueda volver más tarde y probar filtros distintos sin re-ejecutar BLAST.
    
---

## Tabla de trazabilidad completa `RF → CU → slice → HU`

| RF | CU | Slice | HU |
|---|---|---|---|
| RF-01, RF-02, RF-03, RF-04, RF-05, RF-06 | CU001 | CU001_B1 | **HU01_CU001_B1** |
| RF-07, RF-08, RF-11 | CU001 | CU001_B2 | **HU02_CU001_B2** |
| RF-07 | CU001 | CU001_A1 (cancelación manual) | **HU03_CU001_A1** |
| RF-03 | CU001 | CU001_A2 (BD local no disponible) | **HU04_CU001_A2** |
| RF-06 | CU001 | CU001_E1 (secuencia inválida) | **HU05_CU001_E1** |
| RF-04, RF-06 | CU001 | CU001_E2 (parámetros fuera de rango) | **HU06_CU001_E2** |
| RF-05 | CU001 | CU001_E3 (combinación incompatible) | **HU07_CU001_E3** |
| RF-07 | CU001 | CU001_E4 (fallo modo remoto) | **HU08_CU001_E4** |
| RF-09 | CU002 | CU002_B | **HU09_CU002_B** |
| RF-10 | CU003 | CU003_B | **HU10_CU003_B** |
| RF-10 | CU003 | CU003_A1 (resultado vacío) | **HU11_CU003_A1** |

## Notas sobre el enfoque de este TP

- **Un CU puede implementar varios RF**, y viceversa un mismo RF puede estar realizado por varios slices del mismo CU — por ejemplo RF-06 (validación pre-ejecución) aparece en el slice `B1` de `CU001` cuando la validación pasa y también en los slices `E1` y `E2` cuando falla y corta el flujo. La trazabilidad refleja esa realidad.
- **La unidad mínima de sprint es la HU**, no el CU ni el slice. Por eso las HU tienen un identificador propio (`HU01`, `HU02`, …) además del sufijo de trazabilidad — para que la planificación de sprints pueda referirse a ellas sin ambigüedad.
