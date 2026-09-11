# Historias de Usuario — LocalBlast

Cada historia de usuario detalla **un slice puntual** de un caso de uso (relación 1:1). El identificador de la HU conserva explícitamente el del slice de origen, para que la trazabilidad sea directa: la HU llamada `HU01_CU001_B1` detalla el slice `B1` del caso de uso `CU001`.

Formato de cada HU:

- **Deriva de**: qué CU y qué slice detalla.
- **Realiza**: qué RF materializa este slice (heredados del CU y del slice de origen).
- **Rol – meta – motivo**: "Como … quiero … para …".
- **Criterios de aceptación**: en formato **Given-When-Then**, trazables a la precondición y postcondición del slice.

Para el TP1 se detallan las HU de **todos los slices identificados en los casos de uso** — los tres básicos (`CU001_B1`, `CU001_B2`, `CU002_B`), las tres alternativas (`CU001_A1`, `CU001_A2`, `CU002_A1`) y las cuatro excepciones (`CU001_E1`, `CU001_E2`, `CU001_E3`, `CU001_E4`). En total, 10 historias de usuario.

**Numeración:** las HU se enumeran de forma consecutiva por CU y, dentro de cada CU, en el orden: slices básicos (`B` / `B1`, `B2`) → slices alternativos (`A1`, `A2`, …) → slices de excepción (`E1`, `E2`, …). Así los identificadores acompañan el orden en el que aparecen los slices en [`casos-de-uso.md`](casos-de-uso.md).

---

## HU derivadas de CU001 · Ejecutar una búsqueda BLAST

### HU01_CU001_B1 · Cargar, configurar y validar una búsqueda BLAST

- **Deriva de:** `CU001`, slice `B1` (pasos 1-7 del camino feliz)
- **Realiza:** RF-01, RF-02, RF-03, RF-04, RF-05, RF-06

> **Como** investigador/a,
> **quiero** cargar mi secuencia query, elegir el modo (local o remoto), la base de datos, el programa BLAST y los parámetros pre-búsqueda, y que el sistema valide todo antes de habilitar la ejecución,
> **para** no perder tiempo lanzando búsquedas mal configuradas.

**Criterios de aceptación (Given-When-Then)**

- **CA-01.** Configuración completa y válida en modo remoto:
  - **Given** una secuencia FASTA de proteína válida pegada en el formulario, modo remoto seleccionado, base de datos remota "nr", programa `blastp` y parámetros pre-búsqueda en sus valores por defecto,
  - **When** el investigador presiona "Ejecutar búsqueda",
  - **Then** el sistema valida la secuencia y los parámetros, no muestra errores, y habilita la ejecución de la búsqueda (transición al slice `B2`).

- **CA-02.** Valores por defecto sensatos según el programa:
  - **Given** un formulario donde el investigador acaba de seleccionar el programa `blastp`,
  - **When** la interfaz carga los parámetros pre-búsqueda,
  - **Then** los campos de E-value máximo, matriz de sustitución, tamaño de palabra y penalización de gaps aparecen prellenados con los valores por defecto correspondientes al programa `blastp` (no los mismos que para `blastn`).

- **CA-03.** Base de datos coherente con el modo elegido:
  - **Given** el investigador cambia el modo de "remoto" a "local",
  - **When** el sistema recarga la lista de bases de datos disponibles,
  - **Then** la lista muestra únicamente las bases de datos del catálogo local (leídas de D1), sin las bases estándar de NCBI que aparecían en modo remoto.

---

### HU02_CU001_B2 · Ejecutar la búsqueda BLAST y presentar los resultados

- **Deriva de:** `CU001`, slice `B2` (pasos 8-9 del camino feliz)
- **Realiza:** RF-07, RF-08

> **Como** investigador/a,
> **quiero** que el sistema ejecute la búsqueda en segundo plano y me muestre los resultados en una tabla dentro de la misma vista cuando termine,
> **para** para poder seguir trabajando en la aplicación mientras la búsqueda corre, sin quedarme atado a una pantalla de espera.

**Criterios de aceptación (Given-When-Then)**

- **CA-01.** Ejecución asíncrona con indicador de progreso:
  - **Given** una búsqueda ya configurada y validada (postcondición del slice `B1`),
  - **When** el sistema invoca a BLAST+ en segundo plano,
  - **Then** la interfaz muestra un indicador de progreso visible y permanece navegable — el investigador puede desplazarse dentro de la aplicación sin que la ejecución se interrumpa.

- **CA-02.** Presentación de la tabla al finalizar:
  - **Given** una búsqueda que finalizó correctamente y BLAST+ devolvió al menos un hit,
  - **When** el sistema recibe los resultados,
  - **Then** los presenta en una tabla con al menos las columnas: identificador del hit, score, E-value observado, porcentaje de identidad y porcentaje de cobertura.

---

### HU03_CU001_A1 · Cancelación manual de una búsqueda en curso

- **Deriva de:** `CU001`, slice `A1` (camino alternativo durante el slice `B2`)
- **Realiza:** RF-07

> **Como** investigador/a,
> **quiero** poder cancelar una búsqueda que está en ejecución,
> **para** dejar de esperar y no consumir recursos remotos ni locales cuando me di cuenta que configuré algo mal o el resultado ya dejó de importarme.

**Criterios de aceptación (Given-When-Then)**

- **CA-01.** Cancelación de una búsqueda local:
  - **Given** una búsqueda en modo local que BLAST+ está ejecutando en el servidor (indicador de progreso visible),
  - **When** el investigador presiona "Cancelar",
  - **Then** el sistema aborta el subproceso local de BLAST+, deja la interfaz lista para configurar otra búsqueda desde cero y no muestra tabla de resultados.

- **CA-02.** Cancelación de una búsqueda remota:
  - **Given** una búsqueda en modo remoto que BLAST+ tramita contra NCBI (indicador de progreso visible),
  - **When** el investigador presiona "Cancelar",
  - **Then** el sistema cancela la solicitud a través de BLAST+, deja la interfaz lista para configurar otra búsqueda desde cero y no muestra tabla de resultados.

---

