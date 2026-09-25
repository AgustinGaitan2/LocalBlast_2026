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

### HU02_CU001_E1 · Rechazo de secuencia query con formato inválido

- **Deriva de:** `CU001`, slice `E1` (terminación abrupta detectada en el paso 2)
- **Realiza:** RF-02

> **Como** investigador/a,
> **quiero** recibir un mensaje claro cuando la secuencia que subo o pego no es reconocible,
> **para** poder corregirla de inmediato sin tener que adivinar qué le pasa.

**Criterios de aceptación (Given-When-Then)**

- **CA-01.** Caracter fuera del alfabeto:
  - **Given** un texto pegado como query que contiene al menos un carácter fuera del alfabeto de ADN, ARN o proteína (por ejemplo un dígito o un símbolo de puntuación),
  - **When** el investigador confirma la carga,
  - **Then** el sistema no marca la secuencia como cargada, no habilita los controles del `CU002` y muestra un mensaje que indica cuál es el carácter inválido y en qué posición aparece.

- **CA-02.** FASTA con encabezado sin cuerpo:
  - **Given** un archivo FASTA con una línea de encabezado (`>ID`) pero sin ninguna línea de secuencia debajo,
  - **When** el investigador lo sube,
  - **Then** el sistema no marca la secuencia como cargada, no habilita los controles del `CU002` y muestra el mensaje "El FASTA contiene un encabezado pero ninguna secuencia asociada".

---

## HU derivadas de CU002 · Configurar los parámetros de la búsqueda

### HU03_CU002_B · Configurar modo, base de datos, programa y parámetros pre-búsqueda

- **Deriva de:** `CU002`, slice `B` (pasos 1-4 del camino feliz)
- **Realiza:** RF-03, RF-04, RF-05, RF-06

> **Como** investigador/a,
> **quiero** elegir el modo (local o remoto), la base de datos, el programa BLAST y los parámetros pre-búsqueda sobre la secuencia que ya cargué,
> **para** dejar el formulario listo para pedirle al sistema que lo valide.

**Criterios de aceptación (Given-When-Then)**

- **CA-01.** Configuración completa en modo remoto:
  - **Given** una secuencia de proteína ya cargada en la sesión (postcondición de `CU001`),
  - **When** el investigador elige modo remoto, base de datos `nr`, programa `blastp` y deja los parámetros en su valor por defecto,
  - **Then** el formulario queda completo y el sistema habilita el botón "Validar búsqueda" que dispara `CU003`.

- **CA-02.** Valores por defecto sensatos según el programa:
  - **Given** un formulario donde el investigador acaba de seleccionar el programa `blastp`,
  - **When** la interfaz carga los parámetros pre-búsqueda,
  - **Then** los campos de E-value máximo, matriz de sustitución, tamaño de palabra y penalización de gaps aparecen prellenados con los valores por defecto correspondientes al programa `blastp` (no los mismos que para `blastn`).

- **CA-03.** Base de datos coherente con el modo elegido:
  - **Given** el investigador cambia el modo de "remoto" a "local",
  - **When** el sistema recarga la lista de bases de datos disponibles,
  - **Then** la lista muestra únicamente las bases de datos del catálogo local (leídas de D1), sin las bases estándar de NCBI que aparecían en modo remoto.

---

### HU04_CU002_A1 · Manejo de base de datos local no disponible

- **Deriva de:** `CU002`, slice `A1` (camino alternativo en el paso 2)
- **Realiza:** RF-04

> **Como** investigador/a,
> **quiero** que el sistema me informe claramente cuando la base de datos local que elegí no está en condiciones de ser usada, y me devuelva la lista actualizada para que yo decida,
> **para** no quedarme trabado ni terminar corriendo contra una base equivocada porque el sistema me la sustituyó por su cuenta.

**Criterios de aceptación (Given-When-Then)**

- **CA-01.** Base de datos en proceso de actualización:
  - **Given** modo local seleccionado y una base de datos del catálogo D1 que está en estado "actualizándose" porque P3 la está reconstruyendo en ese momento,
  - **When** el investigador la selecciona en el paso 2,
  - **Then** el sistema muestra el mensaje "La base de datos '\<nombre\>' está siendo actualizada y no puede usarse en este momento" y devuelve al investigador al paso 2 con la lista de bases locales actualizada, **sin** proponer un cambio automático a modo remoto.

- **CA-02.** Base de datos con índice en error:
  - **Given** modo local seleccionado y una base de datos cuyo índice quedó marcado como "con errores" tras un fallo previo de `makeblastdb`,
  - **When** el investigador la selecciona en el paso 2,
  - **Then** el sistema muestra un mensaje que explica que el índice está corrupto y sugiere contactar al administrador de bases de datos, y devuelve al investigador al paso 2.

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
