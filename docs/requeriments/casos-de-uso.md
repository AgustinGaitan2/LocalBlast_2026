# Casos de Uso — LocalBlast

Los casos de uso se redactan en **formato textual estructurado (Cockburn)** — actor, objetivo, precondición, flujo principal, alternativos, excepciones, postcondición — según pide el TP1, y **no** como diagrama gráfico (Mermaid no incluye un tipo de diagrama de casos de uso nativo).

Todos los casos de uso de este documento derivan del proceso profundizado **P1 · Ejecutar búsqueda BLAST** del DFD Nivel 1. Los procesos P2 y P3 quedan documentados a nivel de alcance en el DFD y en el modelo de dominio, pero **no** tienen casos de uso propios en este TP (ver justificación en la sección 5 del [SRS](srs.md#5-selección-de-procesos-a-profundizar)).

Cada caso de uso declara qué requerimientos funcionales realiza. La cadena completa de trazabilidad es:

**RF → CU → slice → HU**

---

## CU001 · Ejecutar búsqueda BLAST

- **Actor principal:** Investigador/a
- **Actor secundario:** Motor **BLAST+** (invocado por el sistema en ambos modos: local, y remoto con la flag `-remote` — es BLAST+ el que se comunica con NCBI del otro lado, nunca directamente nuestra GUI)
- **Objetivo:** Obtener un conjunto de alineamientos de una secuencia query contra una base de datos, con parámetros configurables, y llevarlos a un archivo descargable en el formato elegido.
- **Realiza:** RF-01, RF-02, RF-03, RF-04, RF-05, RF-06, RF-07, RF-08, RF-09, RF-10
- **Precondición:** Existe al menos una base de datos disponible (local, con su entrada en D1, o remota entre las que ofrece NCBI). El investigador accedió a la interfaz web.
- **Disparador:** El investigador decide iniciar una nueva búsqueda BLAST.
- **Garantía de éxito:** El investigador obtiene un archivo con los alineamientos filtrados en su equipo, y la búsqueda queda registrada en el historial del sistema.
- **Garantía mínima:** El sistema nunca lanza una búsqueda con datos que no pasaron validación, ni deja búsquedas parcialmente ejecutadas que consuman recursos indefinidamente.

### Flujo principal (camino feliz)

1. El investigador ingresa la **secuencia query** subiendo un archivo FASTA desde su equipo o pegando la secuencia como texto en el formulario.
2. El investigador elige el **modo de ejecución**: local o remoto (NCBI). La interfaz muestra una única opción, alternativa, para que la decisión sea clara.
3. El investigador selecciona la **base de datos** de una lista: si eligió modo local, aparecen las bases de datos del catálogo del laboratorio (leídas de D1); si eligió modo remoto, las bases de datos estándar de NCBI.
4. El investigador elige el **programa BLAST** a ejecutar (`blastn`, `blastp`, `blastx`, `tblastn`, `tblastx`).
5. El investigador ajusta los **parámetros pre-búsqueda** (E-value máximo, matriz de sustitución, tamaño de palabra, penalización de gaps). La interfaz ofrece valores por defecto sensatos para no obligar al usuario a completarlos.
6. El investigador presiona **Ejecutar búsqueda**.
7. El sistema **valida** que la secuencia sea reconocible como ADN, ARN o proteína, que los parámetros estén dentro de rangos lógicos, y que la combinación de programa BLAST elegido, tipo de la secuencia query y tipo de la base de datos seleccionada sea **compatible** (por ejemplo, no dejar correr `blastp` sobre una secuencia de nucleótidos).
8. El sistema **invoca a BLAST+** en segundo plano con la combinación de opciones armada a partir de la configuración del formulario (programa, ruta de la base de datos, query, parámetros pre-búsqueda, y la flag `-remote` cuando el modo elegido es remoto), y muestra un indicador de progreso sin bloquear la interfaz. La comunicación con los servidores de NCBI, cuando corresponde, la hace BLAST+ internamente por la flag `-remote`; el sistema solo espera su respuesta.
9. Cuando termina, el sistema muestra la **lista de alineamientos** (hits) en una tabla, con columnas mínimas: identificador del hit, score, E-value observado, % identidad, % cobertura.
10. El investigador ajusta los **filtros post-búsqueda** (umbrales de identidad, cobertura, E-value observado, taxonomía). La tabla se re-filtra en el momento, sin volver a correr BLAST.
11. El investigador elige el **formato de descarga** (CSV, JSON, FASTA, tabular BLAST o XML) y presiona **Descargar**.
12. El sistema entrega el archivo con los resultados filtrados y guarda una copia de la búsqueda en el historial (D2).

**Postcondición:** El investigador tiene un archivo con los alineamientos filtrados en su equipo. La búsqueda queda registrada en el historial del sistema.
