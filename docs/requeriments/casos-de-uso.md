# Casos de Uso — LocalBlast

Los casos de uso se redactan en **formato textual estructurado (Cockburn)** — actor, objetivo, precondición, flujo principal, alternativos, excepciones, postcondición — según pide el TP1, y **no** como diagrama gráfico (Mermaid no incluye un tipo de diagrama de casos de uso nativo).

Todos los casos de uso de este documento derivan del proceso profundizado **P1 · Ejecutar búsqueda BLAST** del DFD Nivel 1. Los procesos P2 y P3 quedan documentados a nivel de alcance en el DFD y en el modelo de dominio, pero **no** tienen casos de uso propios en este TP (ver justificación en la sección 5 del [SRS](srs.md#5-selección-de-procesos-a-profundizar)).

Cada caso de uso declara qué requerimientos funcionales realiza. La cadena completa de trazabilidad es:

**RF → CU → slice → HU**

## Enfoque de los casos de uso

Un caso de uso representa **una capacidad discreta que el sistema le brinda al actor** , un objetivo alcanzable , no un trazo secuencial de pasos que el actor tiene que recorrer de punta a punta. Dos consecuencias prácticas de esa definición para este TP:

- **Del proceso P1 salen más de un CU.** Aunque a primera vista parece que "ejecutar una búsqueda BLAST" es un único flujo largo, en realidad la capacidad de correr una búsqueda (`CU001`) y la capacidad de trabajar sobre sus resultados —filtrarlos, exportarlos— (`CU002`) son objetivos distintos del mismo actor. El investigador puede correr una búsqueda una sola vez, y sobre ese resultado usar `CU002` varias veces (probar distintos filtros, descargar en distintos formatos) sin volver a correr BLAST. Modelarlos como un único CU secuencial esconde esa reutilización.
- **Cuando el camino feliz de un CU queda largo, se descompone en slices.** No los CU en sí, sino su flujo principal. Los slices son módulos que aportan valor por sí mismos hacia el objetivo del CU. En este TP, `CU001` se descompone en dos slices básicos (`B1` y `B2`); `CU002` queda como un único slice básico (`B`) porque su flujo es corto.

---

## CU001 · Ejecutar una búsqueda BLAST

- **Actor principal:** Investigador/a
- **Actor secundario:** Motor **BLAST+** (invocado por el sistema en ambos modos: local, y remoto con la flag `-remote` — es BLAST+ el que se comunica con NCBI del otro lado, nunca directamente nuestra GUI)
- **Objetivo:** Obtener un conjunto de alineamientos de una secuencia query contra una base de datos elegida, con parámetros del algoritmo bajo control del usuario, y verlos en la interfaz.
- **Realiza:** RF-01, RF-02, RF-03, RF-04, RF-05, RF-06, RF-07, RF-08
- **Precondición:** Existe al menos una base de datos disponible (local, con su entrada en D1, o remota entre las que ofrece NCBI). El investigador accedió a la interfaz web.
- **Disparador:** El investigador decide iniciar una nueva búsqueda BLAST.
- **Garantía de éxito:** El investigador ve la tabla de alineamientos correspondiente a su búsqueda en la interfaz. Ese conjunto de resultados queda disponible en la sesión para que el investigador lo procese después (típicamente con `CU002`).
- **Garantía mínima:** El sistema nunca invoca a BLAST+ con datos que no pasaron validación, ni deja búsquedas parcialmente ejecutadas consumiendo recursos indefinidamente.

### Flujo principal

1. El investigador ingresa la **secuencia query** subiendo un archivo FASTA desde su equipo o pegando la secuencia como texto en el formulario.
2. El investigador elige el **modo de ejecución**: local o remoto (NCBI). La interfaz muestra una única opción alternativa, para que la decisión sea clara.
3. El investigador selecciona la **base de datos** de una lista: si eligió modo local, aparecen las bases de datos del catálogo del laboratorio (leídas de D1); si eligió modo remoto, las bases estándar de NCBI.
4. El investigador elige el **programa BLAST** a ejecutar (`blastn`, `blastp`, `blastx`, `tblastn`, `tblastx`).
5. El investigador ajusta los **parámetros pre-búsqueda** (E-value máximo, matriz de sustitución, tamaño de palabra, penalización de gaps). La interfaz ofrece valores por defecto sensatos según el programa.
6. El investigador presiona **Ejecutar búsqueda**.
7. El sistema **valida** que la secuencia sea reconocible como ADN, ARN o proteína, que los parámetros estén dentro de rangos lógicos, y que la combinación de programa BLAST elegido, tipo de la secuencia query y tipo de la base de datos seleccionada sea **compatible** (por ejemplo, no dejar correr `blastp` sobre una secuencia de nucleótidos).
8. El sistema **invoca a BLAST+** en segundo plano con la combinación de opciones armada a partir del formulario (programa, ruta de la base de datos, query, parámetros pre-búsqueda, y la flag `-remote` cuando el modo elegido es remoto), y muestra un indicador de progreso sin bloquear la interfaz. La comunicación con NCBI, cuando corresponde, la realiza BLAST+ internamente por la flag `-remote`; el sistema solo espera su respuesta.
9. Cuando termina, el sistema muestra la **lista de alineamientos** (hits) en una tabla, con columnas mínimas: identificador del hit, score, E-value observado, % identidad, % cobertura.

**Postcondición:** El investigador ve la tabla de alineamientos de su búsqueda en la interfaz. Los resultados quedan disponibles en la sesión para que el investigador los use en `CU002` (refinar y descargar) si así lo decide.

### Descomposición en slices

El camino feliz de 9 pasos está en el borde de "largo" y tiene dos módulos con valor propio: dejar una búsqueda configurada y validada (valor: el investigador sabe que su búsqueda es lanzable), y ejecutar y presentar los resultados (valor: el investigador ve los hits). Se divide en dos slices básicos, más los alternativos y de excepción que se explican debajo.

```
CU001 · Ejecutar una búsqueda BLAST
├─ Camino feliz (slices básicos)
│  ├─ CU001_B1  — pasos 1-7:  cargar, configurar y validar la búsqueda
│  └─ CU001_B2  — pasos 8-9:  ejecutar la búsqueda y presentar los resultados
├─ Caminos alternativos (slices A)
│  ├─ CU001_A1  — cancelación manual de la búsqueda en curso
│  └─ CU001_A2  — base de datos local no disponible
└─ Terminaciones abruptas (slices E)
   ├─ CU001_E1  — secuencia query con formato inválido
   ├─ CU001_E2  — parámetros pre-búsqueda fuera de rango
   ├─ CU001_E3  — combinación programa / query / base de datos incompatible
   └─ CU001_E4  — fallo del modo remoto de BLAST+
```

### Slices básicos — descripción

- **`CU001_B1` · Cargar, configurar y validar la búsqueda (pasos 1-7).** El investigador ingresa la secuencia query, elige el modo (local o remoto), la base de datos, el programa BLAST y los parámetros pre-búsqueda; al presionar **Ejecutar búsqueda**, el sistema valida el alfabeto de la secuencia, los rangos de los parámetros y la compatibilidad entre programa/query/base de datos. **Valor entregado:** una búsqueda queda configurada y validada, lista para ser ejecutada. **Realiza:** RF-01, RF-02, RF-03, RF-04, RF-05, RF-06.
- **`CU001_B2` · Ejecutar la búsqueda y presentar resultados (pasos 8-9).** El sistema invoca a BLAST+ con la configuración ya validada, muestra un indicador de progreso sin bloquear la interfaz y, al terminar, presenta la tabla de alineamientos con las columnas mínimas. **Valor entregado:** el investigador ve los alineamientos que BLAST+ devolvió para su búsqueda. **Realiza:** RF-07, RF-08.

### Slices alternativos — descripción

Son caminos válidos alternativos al flujo principal; el sistema sigue funcionando y el CU puede alcanzar (o no) el objetivo por otra ruta.

- **`CU001_A1` · Cancelación manual de la búsqueda.** Mientras la búsqueda está en ejecución (durante `CU001_B2`), el investigador presiona **Cancelar**. El sistema aborta el subproceso local o cancela la solicitud remota a través de BLAST+, y deja la interfaz lista para iniciar una nueva búsqueda. La postcondición del CU no se alcanza; es una decisión explícita del actor de abandonar el objetivo actual. **Realiza:** RF-07.
- **`CU001_A2` · Base de datos local no disponible.** En el paso 3, el investigador seleccionó modo local y una base de datos que en ese momento no está lista en D1 (por ejemplo, se está actualizando desde P3, o su índice quedó marcado con error). El sistema informa el estado de esa base de datos y su motivo, y devuelve al investigador al paso 3 con la lista de bases de datos locales actualizada. El investigador decide por su cuenta qué hacer a continuación (elegir otra base local, cambiar de modo, o cancelar); el sistema **no** propone equivalencias entre bases locales y remotas, porque no las hay: una base propia del laboratorio no es intercambiable con las bases estándar de NCBI. **Realiza:** RF-03.


### Slices de excepción — descripción

Son terminaciones abruptas del flujo: el sistema detecta una condición que impide continuar, corta la ejecución del CU y notifica al investigador. La postcondición del CU no se alcanza.

- **`CU001_E1` · Secuencia query con formato inválido.** En el paso 7, la validación detecta que la secuencia ingresada no tiene formato reconocible (caracteres fuera del alfabeto de ADN/ARN/proteína, FASTA mal formado, encabezado sin cuerpo, longitud fuera de rango). El sistema no invoca a BLAST+, corta el flujo y muestra un mensaje que indica exactamente el problema y dónde aparece. **Realiza:** RF-06.
- **`CU001_E2` · Parámetros pre-búsqueda fuera de rango.** En el paso 7, la validación detecta al menos un parámetro con valor imposible (E-value negativo, tamaño de palabra fuera del rango soportado, penalización de gap fuera de escala). El sistema corta el flujo y señala qué campo corregir y cuál es el rango esperado. **Realiza:** RF-04, RF-06.
- **`CU001_E3` · Combinación programa / query / base de datos incompatible.** En el paso 7, la verificación de compatibilidad detecta que el programa BLAST elegido no coincide con el tipo de la secuencia query o con el tipo de la base de datos seleccionada (por ejemplo `blastp` con query de nucleótidos, o `blastn` contra una base de datos de proteínas). El sistema corta el flujo, indica el motivo de la incompatibilidad y sugiere qué combinaciones sí son válidas para lo que el usuario ya cargó. **Realiza:** RF-05.
- **`CU001_E4` · Fallo del modo remoto de BLAST+.** En el paso 8, con modo remoto seleccionado, BLAST+ reporta un error de comunicación con NCBI (sin respuesta, timeout, o error explícito devuelto por la API). El sistema captura el error de BLAST+, corta el flujo del CU e informa al investigador con el detalle del error. Un reintento posterior es un CU nuevo, no la continuación de este. **Realiza:** RF-07.

---

## Trazabilidad RF → CU → slice

La tabla completa `RF → CU → slice → HU` (con las HU incluidas) está en [`historias-usuario.md`](historias-usuario.md). Acá se resume la parte `RF → CU → slice`:

| RF | CU | Slice(s) que lo realizan |
|---|---|---|
| RF-01 | CU001 | B1 |
| RF-02 | CU001 | B1 |
| RF-03 | CU001 | B1, A3 |
| RF-04 | CU001 | B1, E2 |
| RF-05 | CU001 | B1, E3 |
| RF-06 | CU001 | B1, E1, E2 |
| RF-07 | CU001 | B2, A1, E4 |
| RF-08 | CU001 | B2 |
| RF-09 | CU001 | B3, A2 |
| RF-10 | CU001 | B3, A2 |

Un mismo RF puede aparecer en varios slices — por ejemplo RF-06 (validación pre-ejecución) se realiza parcialmente en el camino feliz (`B1`, cuando la validación pasa) y también en las excepciones `E1` y `E2` (cuando la validación falla y corta el flujo).
