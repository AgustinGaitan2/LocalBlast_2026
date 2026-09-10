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



## 3. Requisitos Específicos

### 3.1 Requisitos Funcionales: Detalle estructurado de las entradas, procesos y salidas de cada funcionalidad (casos de uso, historias de usuario).

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
