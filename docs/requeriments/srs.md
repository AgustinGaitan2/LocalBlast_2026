# SRS — LocalBlast

**Especificación de Requerimientos de Software (SRS)**
Este documento es la línea base del proyecto **LocalBlast** al cierre del TP1. Se estructura en secciones y se apoya en documentos hermanos para el detalle de diagramas, casos de uso e historias de usuario.

---

## Índice

1. [Visión y alcance](#1-visión-y-alcance)
2. [Stakeholders y usuarios](#2-stakeholders-y-usuarios)
3. [Diagrama de contexto (DFD)](#3-diagrama-de-contexto-dfd)
4. [Modelo de dominio](#4-modelo-de-dominio)
5. [Selección de procesos a profundizar](#5-selección-de-procesos-a-profundizar)
6. [Requerimientos funcionales](#6-requerimientos-funcionales)
7. [Casos de uso e historias de usuario](#7-casos-de-uso-e-historias-de-usuario)
8. [Suposiciones y dependencias](#8-suposiciones-y-dependencias)
9. [Glosario](#9-glosario)

---

## 1. Visión y alcance

### 1.1 Problema

La ejecución de alineamientos con BLAST presenta hoy dos alternativas incompletas para el usuario típico de un laboratorio o cursada:

- **Línea de comandos (BLAST+):** exige recordar la sintaxis de los binarios (`blastn`, `blastp`, `makeblastdb`, etc.), armar comandos con muchos parámetros, gestionar la ubicación de las bases de datos y parsear la salida a mano. Es la opción más flexible pero tiene barrera de entrada alta.
- **Interfaz web oficial de NCBI:** es accesible pero pesada, no permite ejecutar contra bases de datos propias del laboratorio, y no ofrece filtros interactivos post-búsqueda (identidad, cobertura, taxonomía) sobre la lista de resultados.

Ninguna de las dos permite hoy, con una sola herramienta: correr BLAST **local o remoto** desde la misma interfaz, con **bases de datos propias** del laboratorio administradas por un rol dedicado, aplicar **filtros pre-búsqueda** (parámetros del algoritmo) y **post-búsqueda** (refinamiento sobre resultados) de forma intuitiva, y **descargar los resultados** en el formato que más convenga.

### 1.2 Propuesta de valor

LocalBlast es una **interfaz web para BLAST+** que resuelve las tres carencias:

- El **investigador** decide con un botón si el alineamiento se corre localmente (contra bases de datos del laboratorio) o remotamente. En ambos casos el sistema invoca a BLAST+; en modo remoto le pasa la flag `-remote` y es BLAST+ quien se comunica con NCBI del otro lado.
- El **administrador** puede subir archivos FASTA para dejarlos disponibles como bases de datos locales — sean del propio laboratorio o de bases de datos públicas como SwissProt, que el administrador descarga por su cuenta antes de subirlas al sistema.
- Los **filtros pre-búsqueda** se cargan en un formulario con valores por defecto sensatos; los **filtros post-búsqueda** se aplican en la tabla de resultados sin volver a correr BLAST.
- Los **resultados** se descargan en CSV, JSON, FASTA, tabular BLAST o XML.

### 1.3 Dentro del alcance (TP1 → TP5)

- Interfaz web para investigador y administrador.
- Ejecución de búsquedas BLAST local (`blastn`, `blastp`, `blastx`, `tblastn`, `tblastx`) y remota (`-remote`).
- Formulario de parámetros pre-búsqueda con valores por defecto.
- Aplicación interactiva de filtros post-búsqueda sobre la tabla de resultados.
- Descarga de resultados en múltiples formatos.
- Alta, actualización y baja de bases de datos locales por parte del administrador, a partir de un archivo FASTA subido desde su equipo.
- Autenticación básica con dos roles (Investigador y Administrador).

### 1.4 Fuera del alcance

- Modificación del algoritmo BLAST subyacente. LocalBlast **usa** el motor BLAST+; no lo reimplementa.
- Herramientas de alineamiento múltiple (ClustalW, Muscle) o modelado 3D de estructuras.
- Búsquedas en lote con múltiples queries simultáneas en una sola ejecución (queda como posible ampliación en el Trabajo Integrador).
- Anotación funcional o enriquecimiento biológico de los hits más allá de lo que devuelve BLAST.

---
## 2. Stakeholders y usuarios

| Actor / Stakeholder | Rol | Usa el sistema | Interés en el proyecto |
|---|---|---|---|
| **Investigador/a** | Estudiante de grado/posgrado, tesista, becario/a, docente-investigador/a | Sí (usuario final principal) | Reducir el tiempo de las búsquedas BLAST recurrentes y evitar la fricción de la terminal o de la web de NCBI. |
| **Administrador/a de bases de datos** | Bioinformático/a del laboratorio, técnico/a de IT del grupo de investigación | Sí | Poder mantener bases de datos propias (secuencias del laboratorio) y espejos de bases públicas sin depender del acceso externo. |

---

## 3. Diagrama de contexto (DFD)

Los diagramas de contexto (Nivel 0) y su descomposición (Nivel 1), junto con la descripción de procesos, almacenes y flujos, están en:

👉 [`docs/architecture/contexto-inicial.md`](../architecture/contexto-inicial.md)

---

## 4. Modelo de dominio

El modelo de dominio conceptual, entidades esenciales del problema y sus relaciones sin atributos ni detalles de implementación, está en:

👉 [`docs/requirements/modelo-dominio.md`](modelo-dominio.md)

---

## 5. Selección de procesos a profundizar

De los tres procesos identificados en el DFD Nivel 1 (P1, P2, P3), el grupo elige llevar a profundidad **únicamente P1 (Ejecutar búsqueda BLAST)**. P2 (Filtrar y entregar resultados) y P3 (Administrar bases de datos) quedan documentados a nivel de alcance en el DFD y en el modelo de dominio, pero **no** se detallan como casos de uso propios ni tienen RF profundizados en este SRS.

### 5.1 Qué se profundiza y por qué

- **P1 · Ejecutar búsqueda BLAST — profundizado.** Es el proceso *core* del sistema: sin él no hay valor entregable. Concentra toda la complejidad interesante del dominio (dos modos de invocación a BLAST+ — con o sin `-remote` —, validación de parámetros pre-búsqueda, verificación de compatibilidad programa/query/base de datos, ejecución asíncrona con cancelación, y refinamiento posterior de resultados). Se detalla como `CU001`, descompuesto en slices en [`docs/requirements/casos-de-uso.md`](casos-de-uso.md).

### 5.2 Qué queda fuera del profundizado y por qué

- **P2 · Filtrar y entregar resultados — no profundizado.** Se ejecuta enteramente sobre datos ya en memoria (filtros a la tabla y serialización a un formato) y su lógica es previsible: comparaciones numéricas y export a formatos estándar. En la primera versión del sistema, además, el resultado de P2 es visible como parte del flujo del investigador.

- **P3 · Administrar bases de datos — no profundizado.** Es el proceso de un actor distinto (Administrador), con objetivo distinto y precondición distinta al de P1. Un caso de uso derivado de P3. Ppor ejemplo "Administrar base de datos BLAST local" pertenece conceptualmente a ese proceso, no a P1, y por lo tanto queda fuera de la cadena `RF → CU → slice → HU` de este TP. Se documenta a nivel de alcance en el DFD Nivel 1 (con sus flujos hacia BLAST+ y hacia D1) y sus entidades siguen presentes en el modelo de dominio, pero sin RF ni CU propios profundizados en este cuatrimestre.

**Criterio general.** Esta decisión respeta la recomendación explícita de la cátedra: *"elegir uno bien resuelto vale más que varios a medio desarrollar"*. Concentrar el trabajo en P1 nos permite descomponer su flujo en slices con valor incremental (carga y configuración → ejecución y resultados → refinamiento y descarga), en lugar de dispersar el esfuerzo entre procesos que responden a objetivos y actores diferentes.

---

## 6. Requerimientos funcionales

### Proceso P1 — Ejecución de búsqueda BLAST

| ID | Requerimiento |
|---|---|
| **RF-01** | El sistema debe permitir al usuario ingresar la secuencia query como texto pegado en el formulario o como archivo FASTA subido. |
| **RF-02** | El sistema debe permitir al usuario elegir entre dos modos de ejecución mutuamente excluyentes: **local** (invoca a BLAST+ contra una base de datos del catálogo del laboratorio) o **remoto** (invoca a BLAST+ con la flag `-remote`, y es BLAST+ el que se comunica con NCBI). |
| **RF-03** | El sistema debe permitir al usuario seleccionar una base de datos disponible para el modo elegido: en modo local, las que figuran en el catálogo administrado por P3; en modo remoto, las bases estándar de NCBI. |
| **RF-04** | El sistema debe permitir al usuario configurar los parámetros pre-búsqueda que afectan al algoritmo: **E-value máximo**, **matriz de sustitución** (para BLAST de proteínas), **tamaño de palabra** y **penalización de gaps** (apertura y extensión). El sistema debe ofrecer valores por defecto sensatos según el programa BLAST correspondiente. |
| **RF-05** | El sistema debe permitir al usuario elegir el programa BLAST a ejecutar (`blastn`, `blastp`, `blastx`, `tblastn`, `tblastx`) y debe verificar que esa elección sea compatible con el tipo de la secuencia query y con el tipo de la base de datos seleccionada. Si la combinación no es compatible, no permite lanzar la búsqueda e indica el motivo. |
| **RF-06** | El sistema debe validar, antes de ejecutar la búsqueda, que la secuencia query respete el alfabeto declarado o inferido (ADN, ARN o proteína) y que los parámetros pre-búsqueda estén dentro de rangos válidos. |
| **RF-07** | El sistema debe ejecutar la búsqueda de forma asíncrona, mostrando un indicador de progreso, sin bloquear la interfaz de usuario, y debe permitir cancelar una búsqueda en curso. |

- RF-01: El sistema debe permitir al usuario seleccionar entre ejecución local  o remota.
- RF-02: El sistema debe ejecutar la búsqueda de forma asíncrona, mostrando una barra de progreso o indicador de estado sin bloquear la interfaz de usuario.
- RF-03: El sistema debe aplicar los filtros básicos estándar: E-value máximo, porcentaje de identidad mínimo, porcentaje de cobertura mínimo y matriz de sustitución.
...

### CU-01 · Configurar y lanzar búsqueda BLAST

Actor:           Investigador/a
Objetivo:        Seleccionar el modo de ejecución (local o remoto), ajustar los filtros básicos (E-value, identidad, cobertura, matriz) y poner en marcha la búsqueda de forma asíncrona.
Realiza:         RF-01, RF-02, RF-03
Precondición:    El investigador ya ha cargado una secuencia de consulta válida a través del proceso P1 (Gestionar entrada y validar secuencia).

Flujo principal (slice básico):
  1. El investigador selecciona la base de datos de destino: una de las bases locales prefijadas (ej. "nt", "nr", "swissprot") o la opción "NCBI remoto".
  2. El investigador ingresa los valores de los filtros básicos:
      - E-value máximo (ej. 1e-5)
      - Porcentaje de identidad mínimo (ej. 80)
      - Porcentaje de cobertura mínimo (ej. 70)
      - Matriz de sustitución (BLOSUM62, PAM30, etc.) — solo aplica para BLAST de proteínas.
  3. El investigador hace clic en el botón "Ejecutar búsqueda".
  4. El sistema valida que los parámetros ingresados estén dentro de rangos lógicos (ej. % identidad entre 0 y 100; E-value mayor que cero).
  5. El sistema lanza un hilo en segundo plano para la ejecución y muestra un indicador de progreso (barra de progreso o spinner) sin bloquear la interfaz de usuario.
  6. Según el modo elegido:
      - Si es remoto: el sistema envía la solicitud a la API de NCBI, obtiene un RequestID y comienza el polling periódico (cada 5 segundos) para monitorear el estado del trabajo.
      - Si es local: el sistema construye el comando BLAST+ correspondiente (blastn, blastp, etc.) con los parámetros ingresados y lo ejecuta como subproceso.
  7. El sistema actualiza el indicador de progreso en tiempo real (estado "enviando", "procesando", "finalizando") a medida que avanza la ejecución.

Postcondición: La búsqueda está en curso (o finalizada) en segundo plano, y el investigador puede monitorear su avance o interactuar con otras partes de la interfaz mientras espera.

Slices secundarios nombrados:
  - A1 – Parámetros de filtro fuera de rango: el sistema detecta que algún valor ingresado es inválido (ej. % identidad > 100, E-value negativo) y resalta el campo con un mensaje de error específico, impidiendo el lanzamiento hasta que se corrija.
  - A2 – Cancelación manual durante la ejecución: el investigador puede hacer clic en "Cancelar" en cualquier momento; el sistema aborta el hilo de ejecución (termina el proceso local o cancela la solicitud remota) y muestra un mensaje de cancelación confirmada.


3.2 Requisitos No Funcionales:

Rendimiento: Tiempos de respuesta, volumen de datos.

Seguridad: Autenticación, cifrado de datos.

Usabilidad y Accesibilidad: Diseño de interfaz, curva de aprendizaje.

Disponibilidad y Mantenibilidad: Tolerancia a fallos, soporte.

3.3 Requisitos de Interfaz Externa:

Interfaz de usuario (UI/UX).

Interfaz de software (APIs externas, bases de datos).

Interfaz de hardware o comunicaciones.

## 4. Apéndices / Anexos

Modelos conceptuales, diagramas adicionales (Entidad-Relación, DFDs) o bocetos de interfaz.
