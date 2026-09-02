El diagrama de nivel 0 de este proyecto corresponde a:

```mermaid
graph TD
    U["Investigador/a"]
    N["Servidor NCBI API"]
    F["Repositorio FTP de índices BLAST+"]

    P0(("0<br/>Sistema BLAST Híbrido<br/>"))

    U -->|"Flujo 1: Envía secuencia, parámetros y modo"| P0
    P0 -->|"Flujo 2: Devuelve alineamientos filtrados, gráficas y reportes"| U

    P0 -->|"Flujo 3: Petición QBlast con filtros estándar"| N
    N -->|"Flujo 4: Resultados XML/JSON crudos"| P0

    P0 -->|"Flujo 8a: Solicitud de descarga/actualización de índices"| F
    F -->|"Flujo 8b: Índices BLAST+ descargados"| P0
```

El diagrama de nivel 1 corresponde a:

```mermaid
graph TD
    U["Investigador/a"]
    N["Servidor NCBI API"]
    F["Repositorio FTP de índices BLAST+"]

    P1(("1<br/>Gestionar entrada<br/>y validar secuencia"))
    P2(("2<br/>Ejecutar búsqueda<br/>y aplicar filtros avanzados"))
    P3(("3<br/>Gestionar reportes<br/>y recursos locales"))

    D1[("D1 · Bases de Datos Locales<br/>+ Caché de Resultados")]

    %% FLUJOS EXTERNOS (balanceados con Nivel 0)
    U -->|"Flujo 1: Envía secuencia, parámetros y modo"| P1
    P3 -->|"Flujo 2: Devuelve alineamientos filtrados, gráficas y reportes"| U

    P2 -->|"Flujo 3: Petición QBlast con filtros estándar"| N
    N -->|"Flujo 4: Resultados XML/JSON crudos"| P2

    P3 -->|"Flujo 8a: Descarga/actualización de índices"| F
    F -->|"Flujo 8b: Índices BLAST+ descargados"| P3

    %% FLUJOS INTERNOS
    P1 -->|"Secuencia validada y parámetros de ejecución"| P2
    P2 -->|"Resultados ya filtrados"| P3

    %% FLUJOS CON EL ALMACÉN D1
    P2 -->|"Flujo 5: Ejecuta blast contra índices locales"| D1
    D1 -->|"Retorna hits desde índices locales"| P2

    P2 -->|"Consulta datos de taxonomía para filtrar"| D1
    D1 -->|"Retorna taxonomía de los hits"| P2

    P3 -->|"Flujo 7: Guarda resultados históricos en caché"| D1

    P3 -->|"Registra/actualiza índices descargados"| D1
```
Procesos y entidades:


Del proceso general del sistema P0, se descomponen 3 procesos principales: P1, P2 y P3:
- P1: Gestionar entrada y validar secuencia
Recibe la secuencia cruda y los parámetros del usuario. Verifica el formato (FASTA/RAW), detecta si es ADN o proteína, y confirma que el algoritmo BLAST elegido sea compatible. Entrega la secuencia normalizada y los parámetros listos para ejecutar.
- P2: Ejecutar búsqueda y aplicar filtros avanzados
Es el núcleo operativo. Obtiene los alineamientos en bruto, ya sea consultando la API remota de NCBI o ejecutando BLAST+ contra las bases de datos locales (D1). Inmediatamente después, aplica los filtros combinados (taxonomía, longitud mínima de alineamiento y presencia de gaps) consultando los archivos de linaje en D1. Solo entrega resultados ya depurados.
- P3: Gestionar reportes y recursos locales
Centraliza toda la salida hacia el exterior: genera las gráficas visuales, prepara los reportes descargables (CSV, JSON, PDF y FASTA compilado) para el usuario. Además, mantiene la infraestructura local: guarda resultados en caché (D1) y se encarga de descargar/actualizar los índices BLAST+ desde el FTP cuando es necesario.

- Usuario / Investigador: Persona que envía la consulta y recibe los resultados enriquecidos (gráficos y reportes).

- Servidor NCBI API:  Fuente remota de datos. Recibe peticiones QBlast (Flujo 3) y devuelve resultados en XML/JSON sin filtrar (Flujo 4).

- Repositorio Público FTP:  Fuente externa de índices. Provee los archivos de bases de datos BLAST+ (y taxonomía) para que el sistema pueda funcionar en modo local.

Almacén:
 
- D1:  Bases de Datos Locales + Caché de Resultados: Guarda los índices BLAST (.nhr, .nin, etc.), los archivos de taxonomía (names.dmp/nodes.dmp) y los resultados de búsquedas históricas para reutilización rápida.

Flujos de datos:

- Flujo 1: secuencia + parámetros + modo de ejecución.

- Flujo 2: alineamientos ya filtrados + gráficas + reportes.

- Flujo 3: petición a NCBI con filtros estándar.

- Flujo 4: resultados crudos desde NCBI (sin filtros avanzados).

- Flujo 5: ejecución de BLAST local contra índices.

- Flujo 7: guardado de resultados en caché.

- Flujo 8a: solicitud de descarga/actualización de índices.

- Flujo 8b: entrega de los índices descargados desde el FTP.
