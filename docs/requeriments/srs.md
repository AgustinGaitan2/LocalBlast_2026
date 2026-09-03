## 1. Introducción

### 1.1 Propósito: Objetivo del documento y a quién va dirigido.

### 1.2 Alcance (Scope): Nombre del software, qué hará y qué no hará el sistema.

### 1.3 Definiciones, acrónimos y abreviaturas: Glosario técnico y del dominio.

### 1.4 Referencias: Documentación técnica, estándares o APIs externas consultadas.

### 1.5 Visión general: Organización del resto del documento.

## 2. Descripción General

### 2.1 Perspectiva del producto: Si es un sistema independiente o componente de uno mayor (incluye el diagrama de contexto/nivel 0).

### 2.2 Funciones del producto: Resumen de las funcionalidades principales.

### 2.3 Características y clases de usuarios: Tipos de usuarios y sus niveles de acceso o experiencia.

### 2.4 Entorno operativo: Hardware, sistemas operativos y plataformas requeridas.

### 2.5 Restricciones de diseño e implementación: Lenguajes obligatorios, normativas, límites de rendimiento o frameworks.

### 2.6 Suposiciones y dependencias: Factores externos que se asumen verdaderos para el éxito del desarrollo.

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
