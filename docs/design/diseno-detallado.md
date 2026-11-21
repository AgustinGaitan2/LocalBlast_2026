# Diseño detallado — LocalBlast

**HU08_CU004_B · Ejecutar la búsqueda validada y ver sus resultados**

Este documento baja la arquitectura de LocalBlast ([`architecture.md`](../architecture/architecture.md)) al nivel de clases para una historia de usuario. Parte de la HU y de sus criterios de aceptación, la analiza en sus tres dimensiones (funcionalidad, estructura y calidad) y deriva, en ese orden, el diagrama de robustez, los diagramas de secuencia y el modelo de clases. Cada diagrama sale del anterior: lo que no figura en la robustez no se invoca en las secuencias, y lo que no figura en las secuencias no aparece en el modelo de clases.

---

## Índice

1. [Introducción](#1-introducción)
2. [Relación con la arquitectura](#2-relación-con-la-arquitectura)
3. [Diseño de la HU](#3-diseño-de-la-hu)
4. [Modelo de clases](#4-modelo-de-clases)
5. [Justificación del diseño](#5-justificación-del-diseño)
6. [Implementación](#6-implementación)
7. [Pruebas](#7-pruebas)
8. [Trazabilidad](#8-trazabilidad)
9. [Glosario y bibliografía](#9-glosario-y-bibliografía)

---

## 1. Introducción

### 1.1 Propósito

Definir qué clases, operaciones y colaboraciones implementan la ejecución de una búsqueda BLAST en LocalBlast, desde que el investigador presiona **Ejecutar búsqueda** hasta que ve la tabla de alineamientos y la búsqueda queda guardada en el historial. El documento es la guía para implementar y probar esa funcionalidad.

### 1.2 Historia de usuario elegida

**`HU08_CU004_B` · Ejecutar la búsqueda validada y ver sus resultados**: el camino feliz (pasos 1 a 4) del caso de uso `CU004`. Realiza RF-08, RF-09 y RF-10.

**Qué queda afuera de este diseño:**

- La **cancelación** (`HU09_CU004_A1`) y el **fallo del modo remoto** con su mensaje diferenciado (`HU10_CU004_E1`), que tienen sus propias historias.
- La **identificación del investigador** (autenticación y sesión). No tiene historia de usuario propia y no forma parte de lo que esta HU pide.
- La **validación** de la búsqueda. Es la precondición de la HU (la deja hecha `HU05_CU003_B`), así que aquí la búsqueda llega ya validada.

### 1.3 Motivo de la elección

La HU cumple las tres condiciones para sostener un diseño en tres dimensiones:

| Condición | Evidencia en la arquitectura |
|---|---|
| Está asociada a un escenario de calidad | `EC-01` (concurrencia de invocaciones) y `EC-02` (cambio menor de versión de BLAST+) llegan al componente **Adaptador BLAST+**, que la HU atraviesa (tabla 11.1 de la arquitectura) |
| Atraviesa la estructura | Su recorrido (tabla 11.2) pasa por la Aplicación Web, por las tres capas del Backend y por el sistema externo BLAST+ |
| Hay decisiones de arquitectura que la afectan | `DA-03` (Adaptador BLAST+ dedicado) y `DA-04` (un subproceso por búsqueda) citan al Adaptador; `DA-02` (capas) rige todo el recorrido por el Backend |

Más allá de esas condiciones, es **la historia que justifica la existencia del producto**. LocalBlast es una interfaz para BLAST+, y esta es la única HU en la que BLAST+ se invoca de verdad. Las historias anteriores preparan la búsqueda y las posteriores trabajan sobre resultados que ya existen. Es también la que verifica el driver de la arquitectura (interoperabilidad) y la que tiene más riesgo técnico: ejecutar sin bloquear la interfaz, atender varias búsquedas a la vez sin mezclar resultados e interpretar una salida que no controlamos.

### 1.4 Siglas

| Sigla | Significado |
|---|---|
| BD | Base de datos relacional donde se guarda el historial (no confundir con la entidad `BaseDeDatos`, que es una base de datos BLAST) |
| C4 | Modelo de documentación de arquitectura en cuatro niveles: contexto, contenedores, componentes y código |
| CA | Criterio de aceptación de una historia de usuario |
| CLI | Interfaz de línea de comandos (*command-line interface*) |
| CU | Caso de uso |
| D2 | Almacén del DFD con las búsquedas ejecutadas y sus resultados crudos (historial) |
| DA | Decisión de arquitectura |
| DFD | Diagrama de flujo de datos |
| EC | Escenario de calidad |
| GRASP | Patrones generales para asignar responsabilidades (*General Responsibility Assignment Software Patterns*) |
| HTTP / HTTPS | Protocolo de la web / HTTP sobre una conexión cifrada |
| HU | Historia de usuario |
| JSON | Formato de texto para intercambiar datos estructurados; es el formato de las solicitudes entre la Aplicación Web y el Backend |
| MVC | Modelo-Vista-Controlador |
| NCBI | *National Center for Biotechnology Information*, proveedor del BLAST remoto |
| REST | Estilo de interfaz web basado en recursos y operaciones HTTP; es la interfaz que el Backend ofrece a la Aplicación Web |
| RF | Requerimiento funcional |
| SQL | Lenguaje para consultar y modificar bases de datos relacionales |
| XML | Formato de datos con etiquetas; es la salida de BLAST+ que usa este diseño (`-outfmt 5`) |

---

## 2. Relación con la arquitectura

### 2.1 Tabla de coherencia

| Dimensión | Contenido |
|---|---|
| **Funcionalidad** | `HU08_CU004_B`, slice básico `CU004_B` del caso de uso `CU004 · Ejecutar la búsqueda y ver sus resultados` (pasos 1 a 4). Caminos: el principal (ejecutar, guardar en el historial y mostrar la tabla) y uno de error (BLAST+ no termina bien: no se muestra tabla ni se guarda nada, como exige la garantía mínima de `CU004`). |
| **Estructura** | Contenedor **Aplicación Web** (patrón MVC, `DA-07`): Pantallas, Controlador de búsqueda, Modelo de búsqueda, Modelo de resultados y Cliente del Backend. Contenedor **Backend** (patrón Capas, `DA-02`): **Controladores** (presentación), **Ejecución y persistencia** (dominio), **Acceso a datos** y **Adaptador BLAST+** (datos). Sistema externo **BLAST+**. Estilo base cliente-servidor (`DA-01`). **Componente principal: Ejecución y persistencia.** |
| **Calidad** | `EC-01` · hasta cinco búsquedas concurrentes sin cruce de resultados. Tácticas: *introducir concurrencia* y *encapsular*. Decisión: `DA-04` (un subproceso de BLAST+ por búsqueda). `EC-02` · cambio menor de versión de BLAST+ sin romper la lectura de la salida. Tácticas: *adaptar la interfaz* y *encapsular*. Decisión: `DA-03` (Adaptador BLAST+ dedicado en la capa de datos). |
| **Dominio** | Entidades del modelo de dominio que intervienen: `Busqueda` y `Alineamiento` como clases; `SecuenciaQuery`, `ParametrosPreBusqueda` (con su `VarianteBlast` y su `ModoEjecucion`) y `BaseDeDatos` como datos de la búsqueda. No intervienen `Investigador`, `FiltroPostBusqueda`, `Reporte` ni `FormatoDescarga` (ver [3.2](#32-entidades-del-modelo-de-dominio-que-intervienen)). |
| **Verificación** | `EC-01`: se verificará con una prueba de cinco búsquedas lanzadas a la vez sobre un adaptador simulado con demoras distintas; cada una recibe exactamente sus propios alineamientos (cero cruces). `EC-02`: se verificará con una prueba de la lectura de una salida XML con campos desconocidos; los campos obligatorios llegan intactos y queda registrada una advertencia. Las pruebas concretas se diseñan en la etapa de pruebas, una vez aprobado este diseño. |

### 2.2 Recorrido de la HU sobre los componentes

```mermaid
flowchart LR
    subgraph web["Aplicación Web · MVC"]
        pan["Pantallas"]
        cb["Controlador<br/>de búsqueda"]
        mod["Modelos de búsqueda<br/>y de resultados"]
        cli["Cliente del<br/>Backend"]
    end
    subgraph be["Backend · Capas"]
        subgraph pres["Presentación"]
            ctrl["Controladores"]
        end
        subgraph dom["Dominio"]
            eje["Ejecución y<br/>persistencia ★"]
        end
        subgraph dat["Datos"]
            acc["Acceso a datos"]
            ada["Adaptador BLAST+"]
        end
    end
    blast["BLAST+<br/>(sistema externo)"]

    pan --> cb --> cli
    cb --> mod
    cli -->|JSON / HTTPS| ctrl
    ctrl --> eje
    eje --> ada
    eje --> acc
    ada -->|CLI / subproceso| blast
```

★ componente principal de la HU.

La verificación completa de coherencia con la arquitectura está en la [sección 3.6](#36-verificación-de-coherencia-con-la-arquitectura), porque necesita los diagramas de robustez y de secuencia.

---

## 3. Diseño de la HU

### 3.1 Enunciado y criterios de aceptación

> **Como** investigador/a,
> **quiero** que el sistema invoque a BLAST+ en segundo plano sobre mi búsqueda validada, con indicador de progreso y opción de cancelar, y que al terminar me muestre los alineamientos en una tabla y guarde automáticamente la búsqueda en el historial,
> **para** poder seguir trabajando en la aplicación mientras la búsqueda corre, ver los resultados apenas estén listos y no perder la búsqueda aunque no llegue a refinarla ni descargarla en esta sesión.

- **CA-01. Ejecución asíncrona con indicador de progreso.** **Given** una búsqueda ya configurada y validada (postcondición de `CU003`), **When** el investigador presiona "Ejecutar búsqueda" y el sistema invoca a BLAST+ en segundo plano, **Then** la interfaz muestra un indicador de progreso visible y permanece navegable: el investigador puede desplazarse dentro de la aplicación sin que la ejecución se interrumpa.
- **CA-02. Presentación de la tabla al finalizar.** **Given** una búsqueda en ejecución que BLAST+ termina exitosamente, **When** el sistema recibe el conjunto crudo de alineamientos, **Then** presenta los resultados en una tabla con al menos las columnas: identificador del hit, score, E-value observado, porcentaje de identidad y porcentaje de cobertura.
- **CA-03. Persistencia automática en el historial.** **Given** una búsqueda que BLAST+ terminó exitosamente, **When** el sistema recibe su conjunto crudo de alineamientos, **Then** registra en el historial (D2), antes de presentar la tabla, una entrada con los parámetros pre-búsqueda, la base de datos usada, el timestamp y el conjunto **completo** de resultados crudos que devolvió BLAST+ (antes de cualquier filtro post-búsqueda), sin que el investigador tenga que ejercer `CU005` ni `CU006` para que la persistencia ocurra.

> **Precisión de CA-03.** La redacción original registraba la búsqueda "cuando el sistema termina de mostrar" la tabla. Eso chocaba con la garantía mínima de `CU004` ("si la tabla se muestra, la entrada en D2 también queda escrita"): si se muestra primero y se guarda después, una falla entre los dos pasos deja una tabla visible sin entrada en el historial. Se invirtió el orden (primero se guarda, después se muestra) en [`historias-usuario.md`](../requeriments/historias-usuario.md) y en el flujo de `CU004` de [`casos-de-uso.md`](../requeriments/casos-de-uso.md).

**La búsqueda no se guarda antes de ejecutarse.** La secuencia y la configuración validadas las conserva la Aplicación Web (en su Modelo de búsqueda) y viajan completas en la solicitud de ejecución. La única escritura en la base es la del historial, cuando BLAST+ ya terminó (RF-10).

### 3.2 Entidades del modelo de dominio que intervienen

Se marcaron los sustantivos del enunciado y de los criterios ("búsqueda validada", "BLAST+", "alineamientos", "tabla", "historial", "parámetros pre-búsqueda", "base de datos usada", "timestamp", "resultados crudos", "identificador del hit", "score", "E-value", "porcentaje de identidad", "porcentaje de cobertura") y se buscaron en el [modelo de dominio](../requeriments/modelo-dominio.md). En verde, las entidades que intervienen. El diagrama muestra la parte del modelo que está dentro del alcance de implementación: se omiten `Usuario` y `Administrador`, porque la administración del catálogo de bases no se implementa (ver la [nota sobre el alcance](../requeriments/modelo-dominio.md#nota-sobre-el-alcance) del modelo).

```mermaid
classDiagram
    class Investigador
    class Busqueda
    class SecuenciaQuery
    class ParametrosPreBusqueda
    class VarianteBlast
    class ModoEjecucion
    class BaseDeDatos
    class Alineamiento
    class FiltroPostBusqueda
    class Reporte
    class FormatoDescarga
    Investigador "1" --> "*" SecuenciaQuery : carga
    Investigador "1" --> "*" Busqueda : lanza
    Busqueda "*" --> "1" SecuenciaQuery : usa
    Busqueda "1" *-- "1" ParametrosPreBusqueda : configurada con
    Busqueda "*" --> "1" BaseDeDatos : consulta
    Busqueda "1" *-- "*" Alineamiento : produce
    Busqueda "1" --> "*" Reporte : origina
    ParametrosPreBusqueda "*" --> "1" VarianteBlast : usa la variante
    ParametrosPreBusqueda "*" --> "1" ModoEjecucion : se ejecuta en
    BaseDeDatos "*" --> "1" ModoEjecucion : disponible en
    FiltroPostBusqueda "*" --> "*" Alineamiento : deja visibles
    Reporte "*" --> "*" Alineamiento : incluye los visibles
    Reporte "*" --> "*" FiltroPostBusqueda : registra los aplicados
    Reporte "*" --> "1" FormatoDescarga : exportado en
    style Busqueda fill:#dcfce7,stroke:#15803d
    style SecuenciaQuery fill:#dcfce7,stroke:#15803d
    style VarianteBlast fill:#dcfce7,stroke:#15803d
    style ParametrosPreBusqueda fill:#dcfce7,stroke:#15803d
    style ModoEjecucion fill:#dcfce7,stroke:#15803d
    style BaseDeDatos fill:#dcfce7,stroke:#15803d
    style Alineamiento fill:#dcfce7,stroke:#15803d
```

| Entidad del modelo | ¿Interviene? | Qué usa la HU de ella | La HU la... |
|---|---|---|---|
| `Busqueda` | Sí, como clase | Su configuración, para invocar a BLAST+; los alineamientos que produce; el momento en que se ejecutó | Crea (a partir de la configuración validada) |
| `Alineamiento` | Sí, como clase | Identificador del hit, score, E-value, % identidad y % cobertura: las cinco columnas de la tabla | Crea |
| `SecuenciaQuery` | Sí, como dato de `Busqueda` | El texto FASTA que recibe BLAST+ y su longitud (para la cobertura) | Consulta |
| `ParametrosPreBusqueda` | Sí, como dato de `Busqueda` | E-value máximo, tamaño de palabra, matriz y penalizaciones de gap, y la variante y el modo elegidos | Consulta |
| `VarianteBlast` | Sí, como dato de `ParametrosPreBusqueda` | Qué variante de BLAST+ se invoca (`blastn`, `blastp`, …) | Consulta |
| `ModoEjecucion` | Sí, como dato de `ParametrosPreBusqueda` | Si la invocación lleva la flag `-remote` | Consulta |
| `BaseDeDatos` | Sí, como dato de `Busqueda` | Su ubicación (ruta del índice local o nombre de la base de NCBI) | Consulta |
| `Investigador` | No | La identificación del investigador queda afuera de esta HU (1.2) | — |
| `FiltroPostBusqueda` | No | CA-03 exige guardar el conjunto **crudo**; filtrar es `HU11_CU005_B` | — |
| `Reporte`, `FormatoDescarga` | No | Descargar es `HU12_CU006_B` | — |

**Por qué cinco entidades intervienen solo como datos.** `SecuenciaQuery`, `ParametrosPreBusqueda`, `VarianteBlast`, `ModoEjecucion` y `BaseDeDatos` tienen reglas propias (alfabeto, rangos, compatibilidad entre programa, query y base), pero esas reglas pertenecen a las HU de carga, configuración y validación (`HU01` a `HU07`). Esta HU solo lee sus valores para pasárselos a BLAST+ y guardarlos en el historial. Alcanza con que `Busqueda` los exponga como atributos (la configuración que recibe); convertirlas en clases acá agregaría clases sin comportamiento.

**Cambios al modelo de dominio.** Al armar esta tabla se detectó que el modelo no tenía el concepto de variante de BLAST (hoy `VarianteBlast`) y que tenía multiplicidades que contradecían a `CU001` (una misma secuencia se usa en varias búsquedas). En una segunda revisión se reorganizaron las relaciones para que no pasen todas por `Busqueda`: la variante y el modo cuelgan ahora de `ParametrosPreBusqueda` (se eligen en la misma configuración previa), y `FiltroPostBusqueda` se conecta con `Alineamiento` y con `Reporte`, que es lo que realmente toca, en lugar de con `Busqueda`. Los cambios están en el *Registro de cambios* de [`modelo-dominio.md`](../requeriments/modelo-dominio.md#registro-de-cambios) (cambios 1 a 11). También se renombró `ProgramaBlast` a `VarianteBlast`, porque el nombre anterior se confundía con BLAST+.

### 3.3 Análisis tridimensional

| Elemento | Funcionalidad (qué hace) | Estructura (con qué se hace) | Calidad (qué propiedad cumple) |
|---|---|---|---|
| **CA-01** | Lanzar la búsqueda sin bloquear la interfaz y mostrar un indicador de progreso hasta que llegue la respuesta | `PantallaBusqueda` (delega y muestra el estado de los Modelos); `ControladorBusqueda` (marca la búsqueda en ejecución en `ModeloBusqueda` y pide la ejecución a `ClienteBackend` de forma asíncrona); `ControladorEjecucion` | La interfaz sigue navegable mientras BLAST+ corre, porque nadie en el cliente se queda bloqueado esperando la respuesta |
| **CA-02** | Al terminar BLAST+, mostrar la tabla con hit, score, E-value, % identidad y % cobertura | `AdaptadorBlast` (invoca y lee la salida); `Busqueda` y `Alineamiento`, que calcula sus porcentajes; en el cliente, `ControladorBusqueda` carga las filas en `ModeloResultados` y `PantallaBusqueda` las dibuja al observar el cambio | `EC-02`: si la salida trae campos nuevos, la tabla igual sale con los campos obligatorios intactos |
| **CA-03** | Guardar en el historial la búsqueda con parámetros, base, timestamp y todos los alineamientos crudos | `RepositorioHistorial` (arma el registro a partir de `Busqueda`) y `ConexionBD` (lo escribe en la base en una transacción) | Nunca se muestra una tabla sin su entrada en el historial: primero se guarda y después se devuelve la tabla |
| **`EC-01`** · Concurrencia | Hasta cinco investigadores ejecutan a la vez | Cada solicitud se atiende en su propio hilo del servidor; `AdaptadorBlast` lanza un subproceso propio por búsqueda | **Cero cruces de resultados**: los resultados vuelven por la misma llamada que los pidió, sin estado compartido entre búsquedas |
| **`EC-02`** · Cambio de versión de BLAST+ | BLAST+ devuelve campos que el sistema no conoce | `AdaptadorBlast`, que es el único que conoce el formato de la salida | El 100 % de las salidas "casi conocidas" conserva los campos obligatorios y deja una advertencia en el log |

Los escenarios de **tolerancia a fallos** (rate limit y timeout de NCBI) describen el error del modo remoto, que es `HU10_CU004_E1`. Los de **confidencialidad** dependen de la identificación del investigador, que queda afuera de esta HU. Los de **operabilidad** alcanzan a la configuración (`HU05`) y al filtrado (`HU11`).

### 3.4 Diagrama de robustez

Leyenda: borde punteado = actor o sistema externo; cilindro gris = almacén de datos; rectángulo redondeado azul = *boundary*; círculo naranja = *controller*; rectángulo con barras verde = *entity*. Los recuadros grises agrupan los elementos de cada contenedor y el recuadro verde punteado, el agregado `Busqueda`. Cada flecha dice qué le pide un elemento a otro.

```mermaid
%%{init: {"flowchart": {"nodeSpacing": 60, "rankSpacing": 60}}}%%
flowchart LR
    inv["Investigador/a<br/>(actor)"]

    subgraph web["Aplicación Web (MVC)"]
        ui(["«boundary»<br/>PantallaBusqueda"])
        cb(("«controller»<br/>ControladorBusqueda"))
        mb[["«entity»<br/>ModeloBusqueda"]]
        mr[["«entity»<br/>ModeloResultados"]]
        cl(("«controller»<br/>ClienteBackend"))
    end

    subgraph be["Backend (Capas)"]
        ce(("«controller»<br/>ControladorEjecucion"))
        ab(["«boundary»<br/>AdaptadorBlast"])
        rh(("«controller»<br/>RepositorioHistorial"))
        cbd(["«boundary»<br/>ConexionBD"])
        subgraph agg["agregado Busqueda"]
            bu[["«entity»<br/>Busqueda"]]
            al[["«entity»<br/>Alineamiento"]]
        end
    end
    db[("Base de datos<br/>historial D2")]
    blast["BLAST+<br/>(sistema externo)"]

    inv -->|presiona Ejecutar| ui
    ui -->|delega la acción| cb
    cb -->|lee la configuración<br/>y cambia el estado| mb
    cb -->|carga las filas| mr
    cb -->|pide la ejecución| cl
    cl -->|JSON / HTTPS| ce
    ce -->|crea y registra<br/>los resultados| bu
    ce -->|pide ejecutar| ab
    ab -->|CLI / subproceso| blast
    ce -->|pide guardar| rh
    rh -->|lee lo que guarda| bu
    rh -->|pide escribir| cbd
    cbd -->|SQL| db

    classDef actor fill:#f3f4f6,stroke:#4b5563,color:#111827,stroke-dasharray: 4 3
    classDef boundary fill:#dbeafe,stroke:#1d4ed8,color:#0f172a
    classDef controller fill:#ffedd5,stroke:#c2410c,color:#0f172a
    classDef entity fill:#dcfce7,stroke:#15803d,color:#0f172a
    classDef store fill:#e5e7eb,stroke:#374151,color:#111827
    class inv,blast actor
    class ui,ab,cbd boundary
    class cb,cl,ce,rh controller
    class mb,mr,bu,al entity
    class db store
    style web fill:#f9fafb,stroke:#9ca3af
    style be fill:#f9fafb,stroke:#9ca3af
    style agg fill:#ffffff,stroke:#15803d,stroke-dasharray: 5 5
```

**Cómo se clasificó cada elemento.**

- **Fronteras.** Hay tres, una por cada cosa con la que el sistema habla y que no es código nuestro: el investigador, a través de `PantallaBusqueda`; BLAST+, a través de `AdaptadorBlast`; y el motor de base de datos, a través de `ConexionBD`. La base de datos es un contenedor de LocalBlast, pero no tiene lógica nuestra: es un producto de terceros (PostgreSQL) al que se llega por una conexión y un protocolo (SQL). Para el código del Backend es tan externa como BLAST+, y por eso se accede a ella por una frontera y no directamente desde un controlador.
- **Controladores de la Aplicación Web.** `ControladorBusqueda` interpreta la acción del investigador y actualiza los Modelos (rol Controlador del MVC). `ClienteBackend` es el único que sabe hablar con el Backend por HTTP. La comunicación entre la Aplicación Web y el Backend **no** es una frontera: los dos contenedores tienen lógica nuestra y en los dos extremos hay controladores, así que es una coordinación entre controladores.
- **Controladores del Backend.** `ControladorEjecucion` coordina la ejecución. `RepositorioHistorial` sabe **qué** se guarda del historial (arma el registro a partir de la `Busqueda`), y `ConexionBD` sabe **cómo** se habla con el motor (conexión, sentencias SQL y transacción). El repositorio es un controlador técnico: no tiene reglas del negocio, solo coordina el guardado.
- **Entidades del Backend.** `Busqueda` y `Alineamiento`, que salen de la tabla 3.2. Forman un agregado: un alineamiento no existe sin su búsqueda, y desde afuera se accede siempre a través de `Busqueda`. Por eso `Alineamiento` no tiene flechas propias: solo lo crea y lo consulta su `Busqueda`.
- **Entidades de la Aplicación Web.** `ModeloBusqueda` y `ModeloResultados` son el rol Modelo del MVC: la representación, en el cliente, de la `Busqueda` que se va a ejecutar (su configuración validada y su estado) y de sus `Alineamiento` ya calculados (las filas de la tabla). No son entidades nuevas del dominio, sino la copia en el cliente de dos que ya están en el modelo.
- **Base de datos.** Es el almacén donde queda el historial (D2), en el contenedor *Base de datos*. No es una de las tres categorías de la robustez: se dibuja para mostrar dónde terminan los datos, igual que BLAST+. Solo la toca `ConexionBD`.

**Reglas de conexión verificadas.**

| Tipo de conexión | Flechas del diagrama | ¿Permitida? |
|---|---|---|
| Actor → boundary | Investigador → `PantallaBusqueda` | Sí |
| Boundary → controller | `PantallaBusqueda` → `ControladorBusqueda` | Sí |
| Controller → boundary | `ControladorEjecucion` → `AdaptadorBlast`; `RepositorioHistorial` → `ConexionBD` | Sí: el controlador se apoya en fronteras para llegar a un sistema externo |
| Controller → controller | `ControladorBusqueda` → `ClienteBackend` → `ControladorEjecucion` → `RepositorioHistorial` | Sí |
| Controller → entity | `ControladorBusqueda` → `ModeloBusqueda`, `ModeloResultados`; `ControladorEjecucion` → `Busqueda`; `RepositorioHistorial` → `Busqueda` | Sí |
| Boundary → sistema externo o almacén | `AdaptadorBlast` → BLAST+; `ConexionBD` → Base de datos | Sí: es la razón de ser de esas fronteras |
| Boundary → entity | — | No hay ninguna |
| Actor → controller o entity | — | No hay ninguna |

- **La pantalla no se conecta con ninguna entidad en el diagrama.** En la arquitectura, la Vista observa a los Modelos para leer su estado y redibujarse cuando cambia (`DA-07`, relación *Muestra* del catálogo de la Aplicación Web), pero nunca los modifica ni decide con ellos. Esa observación de solo lectura **no se dibuja en la robustez**, porque el diagrama no admite conexiones de una frontera a una entidad. Lo que el diagrama sí muestra es la regla de fondo: toda acción de la pantalla pasa por `ControladorBusqueda`, que es el único que modifica los Modelos. En los diagramas de secuencia la observación aparece como una nota, no como un mensaje.
- **La Vista nunca se conecta con el Backend:** el único camino hacia el servidor es `ControladorBusqueda → ClienteBackend → ControladorEjecucion`.
- `AdaptadorBlast` recibe datos simples y devuelve los hits como datos, no como `Alineamiento`.
- BLAST+ se alcanza solo a través de su frontera, y la base de datos solo a través de `RepositorioHistorial` y `ConexionBD`.

#### 3.4.1 Dónde vive cada regla del negocio

| # | Regla | Dónde vive | Por qué |
|---|---|---|---|
| R1 | % identidad = identidades ÷ longitud del alineamiento × 100; % cobertura = tramo de la query cubierto ÷ longitud de la query × 100 | Entidad `Alineamiento` | Experto: el alineamiento tiene todos los datos para calcularlos. La longitud de la query se la pasa `Busqueda` al crearlo |
| R2 | Al historial va el conjunto **completo** de alineamientos crudos, sin filtrar | Entidad `Busqueda` | Crea un `Alineamiento` por cada hit que devolvió BLAST+ y no descarta ninguno. Es el conjunto que después guarda el repositorio |
| R3 | La tabla se devuelve solo después de que la búsqueda quedó en el historial | `ControladorEjecucion` (orden de los pasos) | Es una regla de coordinación entre dos colaboradores (el repositorio y quien pidió la ejecución), y por eso el orden lo fija el controlador |
| R4 | Si BLAST+ no termina bien, no se muestra tabla ni se guarda nada (garantía mínima de `CU004`) | `AdaptadorBlast` (avisa con `ErrorBlast`) y `ControladorEjecucion` (el error corta el flujo antes de registrar y de guardar) | El Adaptador es quien sabe que BLAST+ falló (código de salida); el controlador no necesita ningún `if`, porque el error interrumpe la secuencia |
| R5 | Los campos de la salida de BLAST+ que no se conocen se ignoran y se advierten, sin tocar los conocidos (`EC-02`) | `AdaptadorBlast` | Táctica *adaptar la interfaz*: el formato de BLAST+ se conoce en un solo lugar (`DA-03`) |
| R6 | La ejecución pasa por los estados *en ejecución*, *finalizada* o *con error*, y la pantalla muestra progreso, tabla o mensaje según el estado | `ModeloBusqueda` (guarda el estado) y `ControladorBusqueda` (lo cambia) | Es estado de la interacción en el cliente, no del dominio. La Vista solo lo lee, al observar el Modelo, para saber qué dibujar |
| R7 | El registro del historial se escribe completo o no se escribe (la búsqueda y todos sus alineamientos en una sola transacción) | `ConexionBD` | Si la escritura falla a la mitad, no puede quedar una búsqueda con parte de sus alineamientos. La transacción es un detalle del motor de base de datos, y solo la frontera hacia la base lo conoce |

Las reglas del dominio (R1 a R5) viven en el Backend. La pantalla no aplica ninguna: solo muestra lo que tienen los Modelos.

#### 3.4.2 Elementos del diagrama y componentes de la arquitectura

| Elemento | Tipo | Contenedor | Componente | Capa / rol |
|---|---|---|---|---|
| `PantallaBusqueda` | boundary | Aplicación Web | Pantallas | Vista (MVC) |
| `ControladorBusqueda` | controller | Aplicación Web | Controlador de búsqueda | Controlador (MVC) |
| `ModeloBusqueda` | entity | Aplicación Web | Modelo de búsqueda | Modelo (MVC) |
| `ModeloResultados` | entity | Aplicación Web | Modelo de resultados | Modelo (MVC) |
| `ClienteBackend` | controller | Aplicación Web | Cliente del Backend | Apoyo (fuera de la tríada MVC) |
| `ControladorEjecucion` | controller | Backend | **Ejecución y persistencia** | Dominio |
| `Busqueda`, `Alineamiento` | entity | Backend | Ejecución y persistencia | Dominio |
| `RepositorioHistorial` | controller | Backend | Acceso a datos | Datos |
| `ConexionBD` | boundary | Backend | Acceso a datos | Datos |
| `AdaptadorBlast` | boundary | Backend | Adaptador BLAST+ | Datos |
| BLAST+ | sistema externo | — | — | — |
| Base de datos (historial D2) | almacén de datos | Base de datos (PostgreSQL) | — | — |

**Nota sobre el componente Controladores del Backend.** El mensaje de `ClienteBackend` a `ControladorEjecucion` llega por HTTP a una ruta del Backend (componente **Controladores**) que solo convierte la solicitud JSON en la llamada a `ejecutar_busqueda` y el resultado en la respuesta JSON. Es código del framework web sin lógica propia, y por eso no se modela como clase. Así el recorrido respeta la cadena del patrón Capas: Controladores → Ejecución y persistencia → Acceso a datos / Adaptador BLAST+.

**Nota sobre la persistencia intercambiable.** Que el historial se pueda guardar en memoria o en una base real sin tocar `ControladorEjecucion` es una decisión de clases (el controlador conocerá al repositorio solo por su interfaz). Se mostrará en el modelo de clases que se obtenga del código; la robustez no la representa con estereotipos.

### 3.5 Diagramas de secuencia

Hay dos diagramas: el camino principal y el camino de error. Ambos usan solo los participantes del diagrama de robustez. **Cada flecha sólida es una llamada a una operación de la clase que la recibe**: el texto de la flecha es el nombre de esa operación, que al implementar pasa al código con ese mismo nombre. Las flechas punteadas son respuestas. Las únicas excepciones son las flechas hacia BLAST+ y hacia la base de datos, que no son clases nuestras: su texto es la línea de comandos o la sentencia con que se las usa.

**Cómo se redibuja la Vista.** Cuando `ControladorBusqueda` cambia un Modelo, la Vista se entera por suscripción (en React, el cambio de estado provoca que el componente se vuelva a dibujar) y lee el estado del Modelo, como fija `DA-07`. Como en la robustez no hay conexión de la pantalla con los Modelos, en las secuencias esa lectura se muestra como una nota seguida de lo que dibuja la pantalla (`mostrar_progreso`, `mostrar_resultados` o `mostrar_error`), y no como un mensaje. El Modelo nunca llama a la Vista: no la conoce.

#### Secuencia 1 · Camino principal

```mermaid
sequenceDiagram
    autonumber
    actor Inv as Investigador/a
    participant UI as PantallaBusqueda
    participant CB as ControladorBusqueda
    participant MB as ModeloBusqueda
    participant MR as ModeloResultados
    participant CL as ClienteBackend
    participant CE as ControladorEjecucion
    participant B as Busqueda
    participant AB as AdaptadorBlast
    participant BL as BLAST+
    participant AL as Alineamiento
    participant RH as RepositorioHistorial
    participant CBD as ConexionBD
    participant BD as Base de datos

    Inv->>UI: presionar_ejecutar()
    UI->>CB: ejecutar()
    CB->>MB: configuracion()
    MB-->>CB: configuracion validada
    CB->>MB: marcar_en_ejecucion()
    Note over UI,MB: la Vista observa el cambio del Modelo<br/>(solo lectura, DA-07) y se redibuja
    UI->>UI: mostrar_progreso()
    CB-)CL: ejecutar_busqueda(configuracion)
    Note over CB,CL: llamada asíncrona: la interfaz<br/>sigue navegable mientras espera (CA-01)
    CL->>CE: ejecutar_busqueda(configuracion)
    CE->>B: Busqueda(configuracion, fecha)
    CE->>AB: ejecutar(variante, secuencia, base_datos, remota, parametros)
    AB->>BL: blastn/blastp/… -query … -db … -outfmt 5 [-remote] (subproceso propio, EC-01)
    BL-->>AB: salida XML
    AB->>AB: leer_salida(salida_xml)
    opt la salida trae campos desconocidos (EC-02)
        AB->>AB: registrar_advertencia(campos)
    end
    AB-->>CE: hits
    CE->>B: registrar_resultados(hits)
    loop por cada hit
        B->>AL: Alineamiento(hit, longitud_query)
    end
    CE->>RH: guardar(busqueda)
    Note over RH: arma el registro: parámetros, base, fecha<br/>y todos los alineamientos crudos (CA-03)
    RH->>CBD: ejecutar_transaccion(registro)
    CBD->>BD: INSERT … (una sola transacción, R7)
    BD-->>CBD: confirmación
    CE->>B: tabla_resultados()
    loop por cada alineamiento
        B->>AL: porcentaje_identidad()
        B->>AL: porcentaje_cobertura()
    end
    B-->>CE: filas
    CE-->>CL: filas
    CL-->>CB: filas
    CB->>MR: cargar(filas)
    CB->>MB: marcar_finalizada()
    Note over UI,MR: la Vista observa el cambio de los Modelos<br/>(solo lectura, DA-07) y se redibuja
    UI->>UI: mostrar_resultados(filas)
    UI-->>Inv: tabla con hit, score, E-value, % identidad y % cobertura
```

Las tácticas de calidad se ven como operaciones concretas:

- **Introducir concurrencia (`EC-01`).** Cada solicitud de ejecución se atiende en su propio hilo del servidor, y en ese hilo `ejecutar` lanza un **subproceso propio** de BLAST+ y espera su salida (`DA-04`). Los hits vuelven por la misma llamada al mismo `ejecutar_busqueda` que los pidió. No hay ningún lugar compartido donde los resultados de dos búsquedas puedan mezclarse.
- **Adaptar la interfaz y encapsular (`EC-02`).** El controlador y las entidades nunca ven el XML de BLAST+. `leer_salida` toma los campos que conoce por su nombre y, si hay otros, el fragmento `opt` muestra cómo se advierten sin romper nada (`DA-03`).

#### Secuencia 2 · Camino de error: BLAST+ no termina bien

```mermaid
sequenceDiagram
    autonumber
    actor Inv as Investigador/a
    participant UI as PantallaBusqueda
    participant CB as ControladorBusqueda
    participant MB as ModeloBusqueda
    participant CL as ClienteBackend
    participant CE as ControladorEjecucion
    participant B as Busqueda
    participant AB as AdaptadorBlast
    participant BL as BLAST+
    participant RH as RepositorioHistorial

    Inv->>UI: presionar_ejecutar()
    UI->>CB: ejecutar()
    CB->>MB: configuracion()
    MB-->>CB: configuracion validada
    CB->>MB: marcar_en_ejecucion()
    Note over UI,MB: la Vista observa el cambio del Modelo<br/>(solo lectura, DA-07) y se redibuja
    UI->>UI: mostrar_progreso()
    CB-)CL: ejecutar_busqueda(configuracion)
    CL->>CE: ejecutar_busqueda(configuracion)
    CE->>B: Busqueda(configuracion, fecha)
    CE->>AB: ejecutar(variante, secuencia, base_datos, remota, parametros)
    AB->>BL: blastn/blastp/… -query … -db … -outfmt 5 [-remote]
    BL-->>AB: código de salida distinto de 0 y mensaje de error
    AB-->>CE: ErrorBlast(mensaje)
    Note over CE,RH: el error corta el flujo: no se registran<br/>resultados ni se llama a guardar (R4)
    CE-->>CL: ErrorBlast(mensaje)
    CL-->>CB: ErrorBlast(mensaje)
    CB->>MB: registrar_error(mensaje)
    Note over UI,MB: la Vista observa el cambio del Modelo<br/>(solo lectura, DA-07) y se redibuja
    UI->>UI: mostrar_error(mensaje)
    UI-->>Inv: mensaje de BLAST+, sin tabla
```

Este camino cubre la garantía mínima de `CU004`: si la ejecución no termina bien, no se muestra ninguna tabla y no se escribe nada en el historial. `RepositorioHistorial` figura en el diagrama justamente para mostrar que no recibe ninguna llamada; `ModeloResultados`, `ConexionBD` y la base de datos no aparecen porque no se usan. El tratamiento específico del error remoto (distinguir un timeout de un rechazo de NCBI) es de `HU10_CU004_E1`.

#### 3.5.1 Asignación de responsabilidades

| Responsabilidad | Quién | Criterio GRASP |
|---|---|---|
| Recibir el clic y mostrar el progreso, la tabla o el error según lo que tengan los Modelos | `PantallaBusqueda` | Bajo acoplamiento: para actuar solo conoce a `ControladorBusqueda`; a los Modelos solo los observa para leer, y no decide nada |
| Interpretar la acción "ejecutar" en el cliente: tomar la configuración, cambiar el estado, pedir la ejecución, cargar el resultado o el error | `ControladorBusqueda` | Controlador (del lado cliente) |
| Conservar la configuración validada y el estado de la ejecución | `ModeloBusqueda` | Experto en información |
| Conservar las filas recibidas para la tabla (y luego filtrarlas, en `HU11`) | `ModeloResultados` | Experto en información |
| Hablar con el Backend por HTTP | `ClienteBackend` | Bajo acoplamiento y alta cohesión: es lo único del cliente que conoce la forma de la interfaz REST |
| Coordinar la ejecución en el servidor: crear la búsqueda, invocar a BLAST+, registrar, guardar y devolver la tabla | `ControladorEjecucion` | Controlador: orquesta sin hacer el trabajo del dominio |
| Crear la `Busqueda` | `ControladorEjecucion` | Creador: es quien recibe la configuración con la que se inicializa |
| Crear los `Alineamiento` a partir de los hits | `Busqueda` | Creador: la búsqueda contiene a sus alineamientos y tiene el dato que les falta (la longitud de la query) |
| Calcular % identidad y % cobertura | `Alineamiento` | Experto en información |
| Armar las filas de la tabla | `Busqueda` | Experto: conoce todos sus alineamientos |
| Invocar a BLAST+ y leer su salida, advirtiendo los campos desconocidos | `AdaptadorBlast` | Bajo acoplamiento (es lo único que conoce a BLAST+) y alta cohesión |
| Armar el registro del historial a partir de la búsqueda y pedir que se escriba | `RepositorioHistorial` | Alta cohesión y bajo acoplamiento: el controlador pide "guardar" sin saber cómo ni dónde se guarda |
| Escribir el registro en la base de datos en una sola transacción | `ConexionBD` | Bajo acoplamiento y alta cohesión: es lo único que conoce el motor de base de datos y SQL |

### 3.6 Verificación de coherencia con la arquitectura

**Cada mensaje entre componentes distintos existe en el catálogo de relaciones.** Los mensajes entre elementos del mismo componente (por ejemplo, `ControladorEjecucion → Busqueda` o `RepositorioHistorial → ConexionBD`) no necesitan una relación en el catálogo.

| Mensaje de la secuencia | Componente origen → destino | Relación del catálogo |
|---|---|---|
| `PantallaBusqueda → ControladorBusqueda`: `ejecutar()` | Pantallas → Controlador de búsqueda | *Delega* ([7.2.2](../architecture/architecture.md#722-catálogo-de-relaciones-de-la-aplicación-web)) |
| Observación de `PantallaBusqueda` sobre `ModeloBusqueda` y `ModeloResultados` (notas de las secuencias) | Pantallas → Modelo de búsqueda y Modelo de resultados | *Muestra*, solo lectura (7.2.2). No se dibuja en la robustez porque el diagrama no admite frontera → entidad |
| `ControladorBusqueda → ModeloBusqueda`: `configuracion()`, `marcar_en_ejecucion()`, `marcar_finalizada()`, `registrar_error()` | Controlador de búsqueda → Modelo de búsqueda | *Actualiza* (7.2.2) |
| `ControladorBusqueda → ModeloResultados`: `cargar()` | Controlador de búsqueda → Modelo de resultados | *Carga resultados* (7.2.2) |
| `ControladorBusqueda → ClienteBackend`: `ejecutar_busqueda()` | Controlador de búsqueda → Cliente del Backend | *Envía* (7.2.2) |
| `ClienteBackend → ControladorEjecucion`: `ejecutar_busqueda()` | Cliente del Backend → Controladores → Ejecución y persistencia | *Solicita* (7.2.2 y 7.1.2) e *Invoca* ([7.1.2](../architecture/architecture.md#712-catálogo-de-relaciones-del-backend)) |
| `ControladorEjecucion → AdaptadorBlast`: `ejecutar()` | Ejecución y persistencia → Adaptador BLAST+ | *Ejecuta* (7.1.2) |
| `AdaptadorBlast → BLAST+` | Adaptador BLAST+ → BLAST+ | *Invoca*, CLI / subproceso (7.1.2) |
| `ControladorEjecucion → RepositorioHistorial`: `guardar()` | Ejecución y persistencia → Acceso a datos | *Persiste* (7.1.2) |
| `ConexionBD → Base de datos` | Acceso a datos → Base de datos | *Lee y escribe*, SQL (7.1.2) |

**Patrones y estilo del TP de arquitectura.**

- **Capas en el Backend (`DA-02`).** El recorrido baja siempre: Controladores → Ejecución y persistencia → Acceso a datos y Adaptador BLAST+. Ningún elemento de la capa de datos llama a uno de dominio; `RepositorioHistorial` recibe la `Busqueda` como parámetro y la traduce a un registro, que es la responsabilidad que el catálogo le da a Acceso a datos. No se saltea ninguna capa.
- **MVC en la Aplicación Web (`DA-07`).** La Vista delega toda acción en el Controlador y a los Modelos solo los observa para leer; solo el Controlador modifica los Modelos; los Modelos no conocen a nadie; el Cliente del Backend solo lo usa el Controlador.
- **Cliente-servidor (`DA-01`).** El único canal entre la Aplicación Web y el Backend es la solicitud JSON / HTTPS de `ClienteBackend`.
- **Tácticas de calidad.** `EC-01` se ve en el subproceso propio que lanza `ejecutar` (`DA-04`); `EC-02`, en `leer_salida` y `registrar_advertencia` del Adaptador (`DA-03`).

### 3.7 Cambios en los documentos anteriores

Al bajar al diseño aparecieron diferencias con documentos anteriores. Se documentan y se actualizaron esos documentos:

| Documento | Cambio | Motivo |
|---|---|---|
| [`modelo-dominio.md`](../requeriments/modelo-dominio.md#registro-de-cambios) | `VarianteBlast` y `ModoEjecucion` cuelgan de `ParametrosPreBusqueda`; `FiltroPostBusqueda` se conecta con `Alineamiento` y `Reporte` en vez de con `Busqueda` (cambios 8 y 9). `ProgramaBlast` se renombra `VarianteBlast` (cambio 11) | Casi todas las relaciones pasaban por `Busqueda`, aunque varias entidades se relacionan entre sí sin pasar por ella. El nombre `ProgramaBlast` se confundía con BLAST+ |
| [`historias-usuario.md`](../requeriments/historias-usuario.md) y [`casos-de-uso.md`](../requeriments/casos-de-uso.md) | Orden de CA-03 de `HU08` y del flujo de `CU004`: primero se guarda en el historial y después se muestra la tabla | Ver la precisión de CA-03 en [3.1](#31-enunciado-y-criterios-de-aceptación) |

---

## 4. Modelo de clases

### 4.1 Diagrama de clases obtenido del código

El diagrama se obtuvo **por ingeniería inversa del código implementado** con `pyreverse` (incluido en `pylint`), que genera Mermaid directamente:

```bash
cd src
pyreverse -o mmd -d ../docs/design/generado -p localblast dominio aplicacion infraestructura interfaz
```

La salida cruda está en [`generado/clases_pyreverse.mmd`](generado/clases_pyreverse.mmd). La herramienta no dibuja las asociaciones que se guardan en atributos privados (por ejemplo, `ControladorEjecucion → AdaptadorBlast`) ni los estereotipos, así que el grupo la revisó y agregó a mano esas relaciones, los estereotipos y los namespaces por contenedor. Lo que sigue es el diagrama revisado; cada clase, atributo y operación existe tal cual en el código. Se omiten los constructores, los métodos privados auxiliares y las clases de arranque (`main.py`) y de datos de demostración.

```mermaid
classDiagram
    direction TB

    namespace AplicacionWeb {
        class PantallaBusqueda {
            <<boundary>>
            -controlador: ControladorBusqueda
            -modelo_busqueda: ModeloBusqueda
            -modelo_resultados: ModeloResultados
            +presionar_ejecutar() None
            +mostrar_progreso() None
            +mostrar_resultados(filas: list~dict~) None
            +mostrar_error(mensaje: str) None
        }
        class ControladorBusqueda {
            -modelo_busqueda: ModeloBusqueda
            -modelo_resultados: ModeloResultados
            -cliente: ClienteBackend
            -lanzar: Callable
            +preparar(configuracion: dict) None
            +ejecutar() None
        }
        class Observable {
            +suscribir(observador: Callable) None
        }
        class ModeloBusqueda {
            -configuracion_validada: dict
            -estado: str
            -error: Optional~str~
            +establecer_configuracion(configuracion: dict) None
            +configuracion() dict
            +estado() str
            +marcar_en_ejecucion() None
            +marcar_finalizada() None
            +registrar_error(mensaje: str) None
            +mensaje_error() Optional~str~
        }
        class ModeloResultados {
            -filas_recibidas: list~dict~
            +cargar(filas: list~dict~) None
            +filas() list~dict~
        }
        class ClienteBackend {
            +url_base: str
            +tiempo_maximo_segundos: float
            +ejecutar_busqueda(configuracion: dict) list~dict~
        }
        class ErrorEjecucion {
            <<exception>>
            +mensaje: str
        }
    }

    namespace Backend {
        class ControladorEjecucion {
            -adaptador_blast: AdaptadorBlast
            -historial: RepositorioHistorial
            -reloj: Callable
            +ejecutar_busqueda(configuracion: dict) list~dict~
        }
        class Busqueda {
            +secuencia: str
            +programa: str
            +base_datos: str
            +remota: bool
            +parametros: dict
            +fecha: datetime
            +alineamientos: list~Alineamiento~
            +longitud_query() int
            +registrar_resultados(hits: list~dict~) None
            +tabla_resultados() list~dict~
        }
        class Alineamiento {
            +hit_id: str
            +descripcion: str
            +score: float
            +evalue: float
            +identidades: int
            +longitud_alineamiento: int
            +query_desde: int
            +query_hasta: int
            +longitud_query: int
            +porcentaje_identidad() float
            +porcentaje_cobertura() float
        }
        class AdaptadorBlast {
            <<interface>>
            +ejecutar(programa, secuencia, base_datos, remota, parametros) list~dict~
        }
        class AdaptadorBlastCli {
            +directorio_binarios: str
            +tiempo_maximo_segundos: float
            +ejecutar(programa, secuencia, base_datos, remota, parametros) list~dict~
            +leer_salida(salida_xml: str) list~dict~
            +registrar_advertencia(campos: list~str~) None
        }
        class AdaptadorBlastSimulado {
            +hits_preparados: dict
            +bases_disponibles: set~str~
            +demora_segundos: float_o_dict
            +hits_por_defecto: list~dict~
            +invocaciones: list~dict~
            +ejecutar(programa, secuencia, base_datos, remota, parametros) list~dict~
        }
        class ErrorBlast {
            <<exception>>
            +mensaje: str
        }
        class RepositorioHistorial {
            <<interface>>
            +guardar(busqueda: Busqueda) None
        }
        class RepositorioHistorialEnMemoria {
            -busquedas: list~Busqueda~
            +guardar(busqueda: Busqueda) None
            +busquedas() tuple~Busqueda~
        }
        class RepositorioHistorialSql {
            +url_conexion: str
            +guardar(busqueda: Busqueda) None
            +cerrar() None
        }
    }

    PantallaBusqueda --> ControladorBusqueda : delega
    PantallaBusqueda ..> ModeloBusqueda : observa
    PantallaBusqueda ..> ModeloResultados : observa
    ControladorBusqueda --> ModeloBusqueda : actualiza
    ControladorBusqueda --> ModeloResultados : carga
    ControladorBusqueda --> ClienteBackend : envía
    Observable <|-- ModeloBusqueda
    Observable <|-- ModeloResultados
    ClienteBackend ..> ErrorEjecucion : lanza
    ClienteBackend ..> ControladorEjecucion : JSON / HTTP

    ControladorEjecucion --> AdaptadorBlast
    ControladorEjecucion --> RepositorioHistorial
    ControladorEjecucion ..> Busqueda : crea
    Busqueda "1" *-- "*" Alineamiento : produce
    AdaptadorBlastCli ..|> AdaptadorBlast
    AdaptadorBlastSimulado ..|> AdaptadorBlast
    AdaptadorBlast ..> ErrorBlast : lanza
    RepositorioHistorialEnMemoria ..|> RepositorioHistorial
    RepositorioHistorialSql ..|> RepositorioHistorial
    RepositorioHistorial ..> Busqueda : guarda
```

**Correspondencia con las secuencias.**

| Clase | Operaciones | Dónde aparecen |
|---|---|---|
| `PantallaBusqueda` | `presionar_ejecutar`, `mostrar_progreso`, `mostrar_resultados`, `mostrar_error` | Secuencias 1 y 2 (`mostrar_resultados` en 1, `mostrar_error` en 2) |
| `ControladorBusqueda` | `ejecutar` | Secuencias 1 y 2. `preparar` es la precondición (ver 4.2, diferencia 2) |
| `ModeloBusqueda` | `configuracion`, `marcar_en_ejecucion`, `marcar_finalizada`, `registrar_error`, `mensaje_error`, `estado` | Las dos primeras en 1 y 2; `marcar_finalizada` en 1; `registrar_error` y `mensaje_error` en 2; `estado` es la lectura de la nota "la Vista observa el cambio" |
| `ModeloResultados` | `cargar`, `filas` | Secuencia 1 |
| `Observable` | `suscribir` | Nota "la Vista observa el cambio y se redibuja" (secuencias 1 y 2) |
| `ClienteBackend`, `ErrorEjecucion` | `ejecutar_busqueda` | Secuencias 1 y 2 (`ErrorEjecucion` en 2) |
| `ControladorEjecucion` | `ejecutar_busqueda` | Secuencias 1 y 2 |
| `Busqueda` | constructor, `longitud_query`, `registrar_resultados`, `tabla_resultados` | Constructor en 1 y 2; el resto en 1 |
| `Alineamiento` | constructor, `porcentaje_identidad`, `porcentaje_cobertura` | Secuencia 1 |
| `AdaptadorBlast` / `AdaptadorBlastCli` | `ejecutar`, `leer_salida`, `registrar_advertencia` | `ejecutar` en 1 y 2; las otras dos en 1 |
| `RepositorioHistorial` | `guardar` | Secuencia 1 |
| `ErrorBlast` | — (lo lanza `ejecutar`) | Secuencia 2 |
| `AdaptadorBlastSimulado`, `RepositorioHistorialEnMemoria`, `RepositorioHistorialSql` | Implementan las interfaces que participan en las secuencias | Secuencias 1 y 2, detrás de su interfaz |

**Clases por componente de la arquitectura.**

| Contenedor | Componente | Clases | Archivo |
|---|---|---|---|
| Aplicación Web | Pantallas | `PantallaBusqueda` | `src/interfaz/cliente/pantalla_busqueda.py` |
| Aplicación Web | Controlador de búsqueda | `ControladorBusqueda` | `src/interfaz/cliente/controlador_busqueda.py` |
| Aplicación Web | Modelo de búsqueda | `ModeloBusqueda` (y `Observable`) | `src/interfaz/cliente/modelo_busqueda.py`, `observable.py` |
| Aplicación Web | Modelo de resultados | `ModeloResultados` | `src/interfaz/cliente/modelo_resultados.py` |
| Aplicación Web | Cliente del Backend | `ClienteBackend`, `ErrorEjecucion` | `src/interfaz/cliente/cliente_backend.py` |
| Backend | Controladores | ninguna (ruta HTTP del framework) | `src/interfaz/rutas.py` |
| Backend | Ejecución y persistencia | `ControladorEjecucion`, `Busqueda`, `Alineamiento` | `src/aplicacion/controlador_ejecucion.py`, `src/dominio/` |
| Backend | Acceso a datos | `RepositorioHistorial`, `RepositorioHistorialEnMemoria`, `RepositorioHistorialSql` | `src/aplicacion/repositorio_historial.py`, `src/infraestructura/repositorio_historial_*.py` |
| Backend | Adaptador BLAST+ | `AdaptadorBlast`, `ErrorBlast`, `AdaptadorBlastCli`, `AdaptadorBlastSimulado` | `src/aplicacion/adaptador_blast.py`, `src/infraestructura/adaptador_blast_*.py` |

### 4.2 Validación del diagrama contra la robustez y las secuencias

Se contrastó el diagrama obtenido del código con el diagrama de clases de diseño (versión anterior de esta sección), con la robustez (3.4) y con las dos secuencias (3.5). Todos los participantes de la robustez y de las secuencias son clases con el mismo nombre, y todos los mensajes son operaciones con el mismo nombre. Las diferencias encontradas y su resolución:

| # | Diferencia | Resolución | Por qué |
|---|---|---|---|
| 1 | La Aplicación Web está escrita en **Python con Tkinter**, no en React | Se actualizó el diseño (D11). **Pendiente:** si el grupo adopta este cambio, actualizar la tecnología del contenedor en `architecture.md` | El grupo decidió implementar el TP4 completo en Python, el lenguaje que domina, y la consigna admite una interfaz de escritorio mínima. Las clases, los roles MVC y los mensajes no cambian: solo la tecnología de la Vista |
| 2 | `ControladorBusqueda.preparar` y `ModeloBusqueda.establecer_configuracion` no estaban en el diseño | Se mantuvieron en el código y se documentan como **sustitutos de la precondición** (HU03 a HU07) | La configuración validada la deja en el Modelo la validación, que no es de esta HU. Para que la pantalla permita ingresar datos (Parte B) hacía falta cargarla; no se agregan a las secuencias porque ocurren antes del paso 1 |
| 3 | `Observable.suscribir` y `ModeloBusqueda.estado` no estaban | Se actualizó el diagrama de clases | Son la forma concreta de la nota "la Vista observa el cambio y se redibuja" (MVC con suscripción, `DA-07`). Los Modelos siguen sin conocer a la Vista |
| 4 | En el cliente el error es `ErrorEjecucion`, no `ErrorBlast` | Se actualizó la secuencia 2 | La Aplicación Web y el Backend son contenedores distintos: el error cruza como respuesta HTTP 502 con el mensaje, y el cliente no puede importar clases del Backend. `ErrorEjecucion` también cubre el caso "Backend caído" |
| 5 | `Busqueda.longitud_query()` es una operación (en el diseño era un dato que se pasaba) | Se actualizó el diagrama de clases | Experto en información: la búsqueda tiene la secuencia, sabe contar sus residuos (sin el encabezado FASTA) y se los pasa a cada `Alineamiento` |
| 6 | `Busqueda` rechaza una query sin residuos (`ValueError`, la ruta responde 422) | Se agregó como invariante de la entidad y se documenta en la secuencia 2 | Sin residuos, R1 dividiría por cero. Es un invariante del dominio, no una validación de formulario, así que vive en la entidad |
| 7 | Los atributos de `Alineamiento` son públicos (en el diseño eran privados) y se agregó `descripcion` | Se actualizó el diagrama | El repositorio necesita leerlos para persistir los resultados crudos (CA-03); `descripcion` (`Hit_def`) hace legible la tabla |
| 8 | `ControladorEjecucion` recibe un `reloj` por constructor | Se actualizó el diagrama | Para que las pruebas fijen la fecha guardada en el historial sin depender del reloj del sistema. Por defecto es `datetime.now` |
| 9 | `AdaptadorBlastSimulado` tiene hits por secuencia, bases disponibles, demora por secuencia e `invocaciones` | Se actualizó el diagrama | Para probar `EC-01` (cada búsqueda debe recibir *sus* hits, con demoras distintas) y para reproducir el camino de error (base inexistente) en la demostración |
| 10 | `AdaptadorBlastCli` valida programa y parámetros contra listas permitidas y tiene un tiempo máximo | Se mantuvo en el código | Defensa del subproceso: aunque la configuración llega validada, el adaptador no lanza un binario o una flag arbitrarios. Los rechazos salen como `ErrorBlast` (mismo camino de la secuencia 2) |
| 11 | `RepositorioHistorialEnMemoria.busquedas` y `RepositorioHistorialSql.cerrar` | Se mantuvieron fuera de la interfaz | Lectura para las pruebas y liberación de conexiones. El controlador no las usa |

Ninguna diferencia cambia la responsabilidad de una clase ni agrega una llamada entre componentes que no esté en el catálogo de relaciones de la arquitectura.

---

## 5. Justificación del diseño

### 5.1 Responsabilidades de las clases principales

| Clase | Responsabilidad | Criterio GRASP |
|---|---|---|
| `ControladorBusqueda` | En el cliente, convierte el clic en la ejecución: toma la configuración del Modelo, cambia el estado, pide la ejecución al Backend en segundo plano y carga el resultado o el error en los Modelos | Controlador; bajo acoplamiento (la Vista no conoce al Backend) |
| `ModeloBusqueda`, `ModeloResultados` | Guardan el estado que la Vista dibuja: configuración y estado de la ejecución, y filas recibidas | Experto en información; alta cohesión |
| `ClienteBackend` | Único punto del cliente que habla HTTP con el Backend | Bajo acoplamiento y alta cohesión |
| `ControladorEjecucion` | Orquesta la ejecución en el servidor: crea la búsqueda, pide la ejecución, hace registrar los resultados, guarda y devuelve la tabla. No tiene ningún `if` (complejidad ciclomática 1) | Controlador; bajo acoplamiento (depende de dos interfaces, no de sus implementaciones) |
| `Busqueda` | Raíz del agregado: guarda la configuración y el momento de ejecución, cuenta los residuos de la query, crea sus alineamientos con todos los hits y arma la tabla | Experto en información y Creador |
| `Alineamiento` | Calcula sus porcentajes | Experto en información |
| `AdaptadorBlast` | Único punto de contacto con BLAST+: lanza el subproceso, lee la salida y advierte los campos que no conoce | Bajo acoplamiento y alta cohesión |
| `RepositorioHistorial` | Interfaz con la base de datos: guarda la búsqueda terminada con todos sus alineamientos. Sus implementaciones deciden dónde | Alta cohesión y bajo acoplamiento; **Polimorfismo** y **Variaciones protegidas** (ver D9) |

Las entidades del dominio tienen comportamiento propio (crear alineamientos, armar la tabla, calcular porcentajes, proteger su invariante): no son anémicas.

### 5.2 Decisiones de diseño

**D1 · La búsqueda no se guarda antes de ejecutarse.** La configuración validada la conserva `ModeloBusqueda` en el cliente y viaja completa en la solicitud de ejecución. `ControladorEjecucion` crea la `Busqueda` en memoria y la única escritura es la del historial, al final. Guardarla antes obligaba a una lectura extra, a un identificador de búsqueda previo y a manejar estados intermedios en el servidor, sin nada que lo pida en la HU.

**D2 · El cliente hace la llamada de forma asíncrona y espera la respuesta.** `ControladorBusqueda` marca la búsqueda *en ejecución* (la Vista muestra el progreso) y pide la ejecución a `ClienteBackend` en un hilo aparte; cuando llega la respuesta, carga los Modelos. Es lo mínimo que cumple CA-01: la interfaz sigue navegable y el servidor nunca inicia la comunicación (`DA-01`). Se descartó que el cliente consulte el estado periódicamente, porque obliga a guardar en el servidor las búsquedas en curso y a tener una segunda operación de consulta. **Costo asumido:** una búsqueda remota muy larga mantiene abierta la solicitud HTTP todo ese tiempo. Si aparecieran cortes por tiempo, se pasaría a la consulta periódica sin cambiar las clases de dominio. Cómo se lanza la tarea en segundo plano se recibe por constructor (`lanzar`), para poder probar el controlador sin hilos.

**D3 · Concurrencia sin estado compartido.** La ruta HTTP es una función `def` (no `async`), así que FastAPI atiende cada solicitud en su propio hilo (hasta cinco a la vez, como pide `EC-01`), y cada hilo lanza y espera su propio subproceso de BLAST+. Los resultados vuelven por la misma llamada que los pidió. Al no existir un registro compartido de búsquedas en curso, no hay dónde puedan cruzarse. El único objeto compartido es el repositorio en memoria, que protege su lista con un candado.

**D4 · Primero guardar, después devolver la tabla.** `ControladorEjecucion` llama a `guardar` antes de `tabla_resultados`. Si guardar falla, la llamada termina con error y el cliente no recibe tabla. Así nunca se muestra una tabla sin su entrada en el historial (CA-03 y garantía mínima de `CU004`).

**D5 · El Adaptador recibe datos simples y devuelve los hits como datos.** `ejecutar` recibe el programa, la secuencia, la base, el modo y los parámetros, y devuelve una lista de hits (diccionarios con los campos conocidos). El Adaptador no conoce las entidades del dominio (una frontera no toca entidades) y el dominio no conoce flags de línea de comandos ni etiquetas XML (`DA-03`). Es `Busqueda` quien convierte cada hit en un `Alineamiento`.

**D6 · Interfaces solo donde hay más de una implementación.** `AdaptadorBlast` tiene la implementación real (`AdaptadorBlastCli`) y una simulada (`AdaptadorBlastSimulado`), que hace falta para probar `EC-01` con demoras controladas y para correr el sistema donde BLAST+ no está instalado. `RepositorioHistorial` tiene la implementación en memoria y la SQL (ver D9). Las demás clases no tienen interfaz porque tienen una sola implementación posible.

**D7 · Salida XML (`-outfmt 5`).** La salida tabular (`-outfmt 6`) tiene columnas por posición, y una columna nueva corre las demás. En XML cada campo tiene nombre. Por eso es el formato que permite cumplir `EC-02`: tomar los campos conocidos por su nombre e ignorar los nuevos. La columna *score* de la tabla es el *bit score* (`Hsp_bit-score`), que es el que muestra NCBI; de cada hit se toma su primer HSP, que BLAST+ ordena como el mejor.

**D8 · `ErrorBlast` en lugar de un valor de retorno especial.** Cuando BLAST+ termina con error, el Adaptador lanza `ErrorBlast` con el mensaje de BLAST+. El error corta la secuencia antes de registrar y de guardar; la ruta HTTP lo convierte en una respuesta 502 con el mensaje, `ClienteBackend` la convierte en `ErrorEjecucion` y `ControladorBusqueda` la registra en `ModeloBusqueda` para que la Vista la muestre. `ControladorEjecucion` no necesita ramas para ese caso.

**D9 · Interfaz con la base de datos, resuelta por polimorfismo.** Si mañana el historial pasa de una base a otra, el programa no debe cambiar. Para eso `ControladorEjecucion` no guarda en ninguna base concreta: llama a `guardar(busqueda)` sobre la interfaz `RepositorioHistorial`, y es la implementación que recibió por constructor la que decide dónde termina la búsqueda. Hay dos:

- `RepositorioHistorialEnMemoria`: guarda en una lista de Python. Sirve para las pruebas y para correr el sistema sin instalar nada.
- `RepositorioHistorialSql`: guarda en una base relacional, con la búsqueda y sus alineamientos en una sola transacción. Usa SQLAlchemy (la tecnología del componente Acceso a datos), así que la misma clase funciona con SQLite (desarrollo y defensa) o con PostgreSQL (producción, según la arquitectura) cambiando solo `url_conexion`.

Elegir una u otra es un argumento del punto de arranque (`--historial memoria` o `--historial sqlite:///localblast.db`). El controlador, las entidades y las secuencias no cambian. Son dos criterios GRASP que se suman a los cinco básicos: **Polimorfismo** (la variación "dónde se guarda" se resuelve con clases distintas que responden a la misma operación, en lugar de un `if` sobre el tipo de base) y **Variaciones protegidas** (la interfaz protege al resto del sistema del punto que puede cambiar). Agregar otra base en el futuro es agregar otra clase que implemente `RepositorioHistorial`, sin tocar las existentes.

**D10 · La Aplicación Web respeta el MVC de la arquitectura.** La Vista (`PantallaBusqueda`) nunca habla con el Backend ni modifica datos: delega cada acción en `ControladorBusqueda`, que actualiza los Modelos y, cuando hace falta, usa `ClienteBackend`. La Vista se redibuja observando a los Modelos, que no la conocen (`DA-07`). Para esta HU alcanza con un controlador y los dos Modelos que la arquitectura ya define; el Controlador de resultados no interviene porque su trabajo (filtrar y descargar) es de `HU11` a `HU13`.

**D11 · La Vista se implementó con Tkinter en lugar de React.** El grupo decidió escribir todo el TP4 en Python, el lenguaje que domina (restricción tecnológica de la arquitectura), y la consigna admite una interfaz de escritorio mínima (por ejemplo, Tkinter). Se mantuvieron las cinco clases de la Aplicación Web con sus roles MVC y sus mensajes; solo cambia la tecnología de `PantallaBusqueda`. La comunicación con el Backend sigue siendo cliente-servidor por HTTP/JSON (`DA-01`): la interfaz arranca el Backend en un hilo y le habla por `http://127.0.0.1:8000`, igual que lo haría la Aplicación Web en el servidor del laboratorio. Como Tkinter no admite que otro hilo toque sus widgets, la Vista no se redibuja dentro del aviso del Modelo: anota que hubo un cambio y se redibuja en el siguiente ciclo de la interfaz. Pasar a React más adelante implica reescribir las clases del cliente en JavaScript, sin tocar el Backend.

### 5.3 Patrones de diseño usados

| Patrón | Problema que resuelve | Dónde está en el diagrama |
|---|---|---|
| **Repository** | Que el controlador guarde la búsqueda sin saber si el historial está en memoria, en SQLite o en PostgreSQL | `RepositorioHistorial` (interfaz) con `RepositorioHistorialEnMemoria` y `RepositorioHistorialSql` |
| **Adapter** (GoF) | BLAST+ habla por línea de comandos y XML; el dominio necesita "ejecutá esto y devolveme los hits". El Adaptador traduce una interfaz en la otra | `AdaptadorBlast` (interfaz) y `AdaptadorBlastCli` (adaptador) |
| **Observer** (GoF), solo en el cliente | Que la Vista se entere de los cambios de los Modelos sin que los Modelos la conozcan (MVC con suscripción, `DA-07`) | `Observable` con `ModeloBusqueda` y `ModeloResultados`; `PantallaBusqueda` se suscribe |

**Se consideraron y se descartaron:**

- **Observer en el Backend** para que el Adaptador avise al controlador cuando BLAST+ termina: sería una llamada de la capa de datos hacia el dominio, prohibida por `DA-02`. Esperar el subproceso en el mismo hilo resuelve lo mismo. (En el cliente sí se usa, porque ahí lo pide el MVC.)
- **Strategy** para el modo local y el remoto: la diferencia es la flag `-remote`, que resuelve BLAST+. Serían dos clases casi idénticas.

---

## 6. Implementación

### 6.1 Estructura del código

```text
src/
├── main.py                         # punto de arranque: elige implementaciones y las inyecta
├── dominio/                        # entidades (no importa nada de las otras capas)
│   ├── busqueda.py                 #   Busqueda
│   └── alineamiento.py             #   Alineamiento
├── aplicacion/                     # controlador del Backend e interfaces (puertos)
│   ├── controlador_ejecucion.py    #   ControladorEjecucion
│   ├── adaptador_blast.py          #   AdaptadorBlast (interfaz) y ErrorBlast
│   └── repositorio_historial.py    #   RepositorioHistorial (interfaz)
├── infraestructura/                # implementaciones de los puertos
│   ├── adaptador_blast_cli.py      #   BLAST+ real, por subproceso y XML
│   ├── adaptador_blast_simulado.py #   doble de BLAST+ (pruebas y demo)
│   ├── datos_demo.py               #   hits de demostración para el simulado
│   ├── repositorio_historial_en_memoria.py
│   └── repositorio_historial_sql.py#   SQLAlchemy: SQLite o PostgreSQL
└── interfaz/
    ├── rutas.py                    # Backend · Controladores: ruta HTTP (FastAPI)
    └── cliente/                    # Aplicación Web (MVC), en Python
        ├── pantalla_busqueda.py    #   Vista (Tkinter)
        ├── controlador_busqueda.py #   Controlador
        ├── modelo_busqueda.py      #   Modelo
        ├── modelo_resultados.py    #   Modelo
        ├── observable.py           #   suscripción de los Modelos
        └── cliente_backend.py      #   Cliente del Backend (HTTP)
tests/                              # misma estructura que src/, más datos/ con salidas XML de BLAST+
```

**Sentido de las dependencias.** `interfaz` → `aplicacion` → `dominio`, e `infraestructura` → `aplicacion` (implementa sus interfaces) y `dominio`. El dominio no importa nada de las demás carpetas, y `aplicacion` no importa nada de `infraestructura` ni de `interfaz`. El cliente (`interfaz/cliente/`) no importa nada del Backend: solo le habla por HTTP. El único archivo que conoce las implementaciones concretas es `main.py`.

**Correspondencia con la arquitectura.** `aplicacion/controlador_ejecucion.py` y `dominio/` son el componente **Ejecución y persistencia**; `aplicacion/repositorio_historial.py` e `infraestructura/repositorio_historial_*` son **Acceso a datos**; `aplicacion/adaptador_blast.py` e `infraestructura/adaptador_blast_*` son el **Adaptador BLAST+**; `interfaz/rutas.py` es **Controladores**; cada archivo de `interfaz/cliente/` es el componente homónimo de la Aplicación Web.

### 6.2 Cómo se ejecuta

Las instrucciones completas (instalación en una máquina limpia, interfaz y pruebas) están en el [`README.md`](../../README.md#3-cómo-instalar-y-ejecutar-tp4). En resumen:

```bash
pip install -r requirements.txt
python src/main.py                    # Backend + interfaz gráfica, con BLAST+ simulado si no está instalado
python -m pytest --cov --cov-branch   # pruebas y cobertura
```

### 6.3 Cómo se reemplazan la persistencia y BLAST+

`main.py` es el único lugar que crea las implementaciones concretas y se las pasa a `ControladorEjecucion` por su constructor:

| Opción | Implementación que se inyecta |
|---|---|
| `--historial memoria` | `RepositorioHistorialEnMemoria` |
| `--historial sqlite:///localblast.db` (por defecto) | `RepositorioHistorialSql` sobre SQLite |
| `--historial postgresql://usuario:clave@host/localblast` | `RepositorioHistorialSql` sobre PostgreSQL (requiere `pip install psycopg2-binary`) |
| `--adaptador cli` (o `auto` con `blastn` en el `PATH`) | `AdaptadorBlastCli` (BLAST+ real; `--blast-bin` indica la carpeta de los binarios) |
| `--adaptador simulado` (o `auto` sin BLAST+) | `AdaptadorBlastSimulado` con los datos de `datos_demo.py` |

En ninguno de los casos cambia `ControladorEjecucion`, las entidades ni la interfaz: es la demostración de D9 que pide la defensa.

---

## 7. Pruebas

Las pruebas son unitarias (pytest) y no pasan por la interfaz gráfica: se prueban las entidades, los controladores (del Backend y del cliente), la ruta HTTP y las implementaciones de los puertos. Los colaboradores se reemplazan por dobles: `AdaptadorBlastSimulado`, `RepositorioHistorialEnMemoria`, un `subprocess.run` falso para el adaptador real y un `urlopen` falso para el cliente HTTP. `RepositorioHistorialSql` se prueba contra un archivo SQLite temporal (prueba de integración liviana, sin instalar nada).

### 7.1 Casos de prueba

CN = caja negra (desde los criterios de aceptación y los escenarios de calidad); CB = caja blanca (desde el código, un caso por camino independiente, ver 7.2). Cada fila es una función `test_cpNN_...` en `tests/`.

| ID | Técnica | Origen | Dado (entrada y estado) | Resultado esperado |
|---|---|---|---|---|
| CP-01 | CN, partición | CA-02, R1 | Hit con 90 identidades en 120 posiciones | % identidad = 75 |
| CP-02 | CN, límite | CA-02, R1 | Identidades = longitud del alineamiento | % identidad = 100 |
| CP-03 | CN, partición | CA-02, R1 | Hit que cubre las posiciones 11 a 60 de una query de 100 | % cobertura = 50 (tramo inclusivo) |
| CP-04 | CN, límite | CA-02, R1 | Hit que cubre la query completa (1 a 250 de 250) | % cobertura = 100 |
| CP-05 | CB | `Alineamiento.__init__` | Hit con valores como texto (así llegan del XML) | Atributos convertidos a `str`, `float`, `int` |
| CP-06 | CN | CA-03 | Configuración completa | La búsqueda guarda programa, base, modo, parámetros y fecha; sin alineamientos |
| CP-07 | CB | `Busqueda.__init__` (rama sin parámetros) | Configuración sin `remota` ni `parametros` | Modo local y parámetros vacíos |
| CP-08 | CN, partición | R1 | Query FASTA con encabezado, saltos de línea y espacios | Longitud = solo residuos (8) |
| CP-09 | CB | `Busqueda.longitud_query` (sin encabezado) | Query en texto plano con un espacio | Longitud = 6 |
| CP-10 | CN, límite | Invariante de `Busqueda` | Query con encabezado y sin residuos | `ValueError` |
| CP-11 | CN | CA-03, R2 | Tres hits, uno con E-value alto y otro con 1 identidad | Tres alineamientos, ninguno descartado |
| CP-12 | CN | R1 | Hit que cubre 25 de los 100 residuos | El alineamiento recibe la longitud de la query (25 %) |
| CP-13 | CB, límite | `registrar_resultados` y `tabla_resultados` (0 vueltas) | BLAST+ sin hits | Tabla vacía |
| CP-14 | CN | CA-02 | Un hit | Fila con hit, descripción, score, E-value, % identidad y % cobertura redondeados |
| CP-15 | CN | CA-02 | Adaptador con dos hits | Dos filas con las columnas de CA-02 |
| CP-16 | CN | Secuencia 1, mensaje `ejecutar` | Configuración remota con parámetros | El adaptador recibe programa, secuencia, base, modo y parámetros |
| CP-17 | CN | CA-03 | Dos hits, reloj fijo | El historial tiene una búsqueda con base, parámetros, fecha y los dos alineamientos crudos |
| CP-18 | CN | CA-03, R3 (D4) | Repositorio que falla al guardar | Error; no se devuelve tabla |
| CP-19 | CN | Garantía mínima de `CU004`, R4 | Base inexistente: BLAST+ falla | `ErrorBlast` con el mensaje; historial vacío |
| CP-20 | CN | Invariante de `Busqueda` | Query sin residuos | `ValueError`; BLAST+ no se invoca y no se guarda nada |
| CP-21 | CN | **`EC-01`** | Cinco búsquedas simultáneas con demoras distintas (0,05 a 0,3 s) | Cada una recibe exactamente sus hits; cinco búsquedas guardadas, cada una con los suyos (**cero cruces**) |
| CP-22 | CN | CA-02 | Salida XML real de BLAST+ 2.14 con dos hits | Hits con los seis campos obligatorios, hit_id y descripción |
| CP-23 | CB | `leer_salida` (sin campos desconocidos) | Salida de 2.14 | Ninguna advertencia en el log |
| CP-24 | CN | **`EC-02`**, R5 | La misma salida con campos nuevos (`Hit_taxid`, `Hsp_cigar`) y versión 2.15 | Hits idénticos a los de CP-22 y **una** advertencia que nombra los campos nuevos |
| CP-25 | CB | `_leer_hit` (falta un obligatorio) | HSP sin E-value, identidad ni posiciones | `ErrorBlast` que nombra los campos faltantes |
| CP-26 | CB | `leer_salida` (XML inválido) | Texto que no es XML | `ErrorBlast` |
| CP-27 | CB | `leer_salida` (hit sin HSP) | Un hit sin HSP | Se ignora (lista vacía) |
| CP-28 | CB, límite | `leer_salida` (0 hits) | Salida sin hits | Lista vacía |
| CP-29 | CN | `DA-03`, D7 | Ejecución local con `evalue` | Comando `blastn -db … -outfmt 5 -evalue …`, query por la entrada estándar |
| CP-30 | CB | `_armar_comando` (modo remoto) | `remota = True` | El comando incluye `-remote` |
| CP-31 | CB | `_armar_comando` (carpeta de binarios) | `directorio_binarios` configurado | Se invoca el binario de esa carpeta |
| CP-32 | CN | R4 | BLAST+ termina con código 2 y mensaje | `ErrorBlast` con el mensaje de BLAST+ |
| CP-33 | CB | `ejecutar` (error sin mensaje) | Código 3 sin texto de error | `ErrorBlast` que informa el código |
| CP-34 | CB | `ejecutar` (`FileNotFoundError`) | BLAST+ no instalado | `ErrorBlast` "No se encontró…" |
| CP-35 | CB | `ejecutar` (`TimeoutExpired`) | Ejecución que supera el tiempo máximo | `ErrorBlast` |
| CP-36 | CB | `_armar_comando` (programa no válido) | Programa `rm` | `ErrorBlast`; no se lanza ningún subproceso |
| CP-37 | CB | `_armar_comando` (parámetro no admitido) | Parámetro `out` | `ErrorBlast`; no se lanza ningún subproceso |
| CP-38 | CB | `AdaptadorBlastSimulado.ejecutar` | Secuencia con hits preparados | Devuelve esos hits |
| CP-39 | CB | `AdaptadorBlastSimulado.ejecutar` | Otra secuencia | Devuelve los hits por defecto |
| CP-40 | CB | `AdaptadorBlastSimulado.ejecutar` | Base no disponible | `ErrorBlast` como el de BLAST+ |
| CP-41 | CB | `_demora_para` (por secuencia) | Demora solo para una secuencia | Una vuelve enseguida y la otra tarda lo indicado |
| CP-42 | CB | `_demora_para` (fija) | Demora fija | La búsqueda tarda lo indicado |
| CP-43 | CN | CA-03 | Dos búsquedas en memoria | Guardadas en orden |
| CP-44 | CN | CA-03 | Búsqueda con dos hits en SQLite | Una fila en `busquedas` (base, fecha, parámetros) y dos en `alineamientos` ligadas a ella |
| CP-45 | CB | `RepositorioHistorialSql.guardar` (sin hits) | Búsqueda sin alineamientos | Se guarda la búsqueda sola |
| CP-46 | CN | CA-03 (atomicidad) | Un alineamiento inválido | Error y **nada** guardado: ni la búsqueda ni sus alineamientos |
| CP-47 | CN | CA-02 | POST con configuración válida | HTTP 200 con las filas |
| CP-48 | CN | R4 | POST con base inexistente | HTTP 502 con el mensaje de BLAST+ |
| CP-49 | CN | Invariante de `Busqueda` | POST con query sin residuos | HTTP 422 |
| CP-50 | CN | CA-01 | Ejecutar, con la respuesta todavía pendiente | Estado *en ejecución* (la Vista muestra el progreso) |
| CP-51 | CN | **CA-01** | Ejecutar con un hilo real y un Backend que no responde hasta que la prueba lo libera | `ejecutar()` vuelve enseguida en estado *en ejecución*; al responder, queda *finalizada* con las filas |
| CP-52 | CN | CA-02, R6 | Llega la respuesta con filas | Filas en `ModeloResultados`, estado *finalizada* |
| CP-53 | CN | R4, R6 | Llega un error | Estado *con error*, mensaje guardado, ninguna fila |
| CP-54 | CN | `DA-07` (suscripción) | Cambios en los dos Modelos | Cada cambio se avisa al suscriptor, en orden |
| CP-55 | CB | `marcar_en_ejecucion` | Nueva ejecución tras un error | El error anterior se borra |
| CP-56 | CN | Relación Cliente del Backend → Backend | Respuesta 200 | Envía la configuración por POST a la URL correcta y devuelve las filas |
| CP-57 | CB | `ClienteBackend.ejecutar_busqueda` (HTTP 502) | Error con cuerpo JSON | `ErrorEjecucion` con el mensaje de BLAST+ |
| CP-58 | CB | `_mensaje_de` (cuerpo no JSON) | Error 500 sin JSON | `ErrorEjecucion` que informa el código |
| CP-59 | CB | `ClienteBackend.ejecutar_busqueda` (sin conexión) | Backend caído | `ErrorEjecucion` "No se pudo conectar…" |
| CP-60 | CB | `AdaptadorBlastSimulado.ejecutar` | Secuencia con un salto de línea al final (así la entrega la pantalla) | Encuentra los hits preparados igual |

**Cada criterio de aceptación llega a una prueba:** CA-01 → CP-50, CP-51; CA-02 → CP-01 a CP-04, CP-14, CP-15, CP-22, CP-47, CP-52; CA-03 → CP-11, CP-17, CP-18, CP-43, CP-44, CP-46. **Cada escenario de calidad tiene la prueba de su medida:** `EC-01` → CP-21; `EC-02` → CP-24.

### 7.2 Complejidad ciclomática

Calculada como decisiones + 1 (`if`, `for`, `except`, `and`/`or`, condiciones de comprensiones) para las operaciones que implementa la HU, y verificada con `radon cc -s src`. Los constructores sin decisiones y las operaciones de complejidad 1 que solo asignan o delegan no se listan, salvo las de la HU.

| Operación | Decisiones | Complejidad | Casos que cubren cada camino |
|---|---|---|---|
| `Alineamiento.porcentaje_identidad` | 0 | 1 | CP-01 (CP-02 es el límite) |
| `Alineamiento.porcentaje_cobertura` | 0 | 1 | CP-03 (CP-04 es el límite) |
| `Busqueda.__init__` | 2 (`parametros or {}`, query sin residuos) | 3 | CP-06 (con parámetros), CP-07 (sin parámetros), CP-10 (sin residuos) |
| `Busqueda.longitud_query` | 2 (`for` e `if` de la comprensión) | 3 | CP-08 (línea de encabezado descartada), CP-09 (sin encabezado), CP-10 (ninguna línea con residuos) |
| `Busqueda.registrar_resultados` | 1 (`for`) | 2 | CP-13 (cero hits), CP-11 (varios hits) |
| `Busqueda.tabla_resultados` | 1 (`for`) | 2 | CP-13 (cero), CP-14 (uno) |
| `ControladorEjecucion.ejecutar_busqueda` | 0 | **1** | CP-15. Sus "rechazos" no son ramas: son excepciones de los colaboradores que cortan la secuencia (CP-18, CP-19, CP-20) |
| `AdaptadorBlastCli.ejecutar` | 4 (`except` × 2, código ≠ 0, `or` del mensaje) | 5 | CP-29, CP-34, CP-35, CP-32, CP-33 |
| `AdaptadorBlastCli.leer_salida` | 6 (`except`, `for`, sin HSP, dos comprensiones, campos desconocidos) | 7 | CP-26, CP-28, CP-27, CP-22/CP-23 (sin desconocidos), CP-24 (con desconocidos), más las dos comprensiones recorridas en CP-22 y CP-24 |
| `AdaptadorBlastCli._leer_hit` | 4 (`for`, comprensión `for` e `if`, faltantes) | 5 | CP-22 (ninguno falta), CP-25 (faltan). Los caminos "cero vueltas" de los `for` no son posibles: los campos obligatorios son siempre seis |
| `AdaptadorBlastCli._armar_comando` | 5 (programa no válido, carpeta de binarios, remota, `for`, parámetro no admitido) | 6 | CP-36, CP-31, CP-30, CP-29 (con parámetros), CP-30 (sin parámetros), CP-37 |
| Ruta `ejecutar_busqueda` (`rutas.py`) | 2 (`except` × 2) | 3 | CP-47, CP-48, CP-49 |
| `ControladorBusqueda.ejecutar` | 0 | 1 | CP-50 |
| `ControladorBusqueda._esperar_resultados` | 1 (`except`) | 2 | CP-52, CP-53 |
| `ClienteBackend.ejecutar_busqueda` | 2 (`except` × 2) | 3 | CP-56, CP-57, CP-59 |
| `ClienteBackend._mensaje_de` | 1 (`except`) | 2 | CP-57, CP-58 |
| `RepositorioHistorialSql.guardar` | 2 (comprensión, `if filas`) | 3 | CP-44, CP-45, CP-46 |

Ninguna operación supera 7, y el controlador del Backend tiene complejidad 1: la secuencia no tiene `alt` porque el error corta el flujo por excepción (D8). Es la señal de que el controlador no hace trabajo del dominio.

### 7.3 Resultados y cobertura

Las 60 pruebas pasan al ejecutarlas desde cero en un entorno virtual nuevo (`python -m pytest`). La cobertura de **sentencias y de ramas es del 100 %** sobre el código medido (dominio, aplicación, infraestructura, ruta HTTP y clases del cliente), con `PantallaBusqueda`, `main.py` y `datos_demo.py` excluidos. El reporte completo y su análisis están en [`cobertura.md`](cobertura.md).

---

## 8. Trazabilidad

### 8.1 HU → componente C4 → clases → archivo → pruebas

Extiende la tabla 11.2 de la arquitectura con las columnas de diseño y de pruebas.

| Criterio / escenario | Componente C4 | Clases | Archivo | Pruebas |
|---|---|---|---|---|
| CA-01 · Ejecución sin bloquear, con progreso | Pantallas → Controlador de búsqueda → Modelo de búsqueda; Controlador de búsqueda → Cliente del Backend → Controladores → Ejecución y persistencia | `PantallaBusqueda`, `ControladorBusqueda`, `ModeloBusqueda`, `ClienteBackend`, `ControladorEjecucion` | `interfaz/cliente/`, `interfaz/rutas.py`, `aplicacion/controlador_ejecucion.py` | CP-50, CP-51, CP-54 (y la demostración con la interfaz) |
| CA-02 · Tabla al finalizar | Ejecución y persistencia → Adaptador BLAST+; Controlador de búsqueda → Modelo de resultados → Pantallas | `ControladorEjecucion`, `AdaptadorBlast`, `Busqueda`, `Alineamiento`, `ControladorBusqueda`, `ModeloResultados`, `PantallaBusqueda` | `aplicacion/controlador_ejecucion.py`, `dominio/busqueda.py`, `dominio/alineamiento.py`, `infraestructura/adaptador_blast_cli.py`, `interfaz/cliente/` | CP-01 a CP-05, CP-08, CP-09, CP-12 a CP-16, CP-22, CP-29, CP-47, CP-52, CP-56 |
| CA-03 · Persistencia en el historial | Ejecución y persistencia → Acceso a datos | `ControladorEjecucion`, `Busqueda`, `RepositorioHistorial` y sus implementaciones | `aplicacion/controlador_ejecucion.py`, `aplicacion/repositorio_historial.py`, `infraestructura/repositorio_historial_en_memoria.py`, `infraestructura/repositorio_historial_sql.py` | CP-06, CP-07, CP-11, CP-17, CP-18, CP-43 a CP-46 |
| Camino de error (garantía mínima de `CU004`) | Ejecución y persistencia → Adaptador BLAST+; Controlador de búsqueda → Modelo de búsqueda → Pantallas | `AdaptadorBlast`, `ErrorBlast`, `ControladorEjecucion`, `ClienteBackend`, `ErrorEjecucion`, `ControladorBusqueda`, `ModeloBusqueda`, `PantallaBusqueda` | `aplicacion/adaptador_blast.py`, `aplicacion/controlador_ejecucion.py`, `infraestructura/adaptador_blast_*.py`, `interfaz/rutas.py`, `interfaz/cliente/` | CP-10, CP-19, CP-20, CP-25, CP-26, CP-32 a CP-37, CP-40, CP-48, CP-49, CP-53, CP-55, CP-57 a CP-59 |
| `EC-01` · Cero cruces con cinco concurrentes | Ejecución y persistencia → Adaptador BLAST+ | `ControladorEjecucion`, `AdaptadorBlast`, `RepositorioHistorialEnMemoria` | `aplicacion/controlador_ejecucion.py`, `interfaz/rutas.py` (`def`, un hilo por solicitud), `infraestructura/adaptador_blast_cli.py` (un subproceso por llamada) | **CP-21**, CP-38, CP-39, CP-41, CP-60 |
| `EC-02` · Campos nuevos en la salida | Adaptador BLAST+ | `AdaptadorBlastCli` | `infraestructura/adaptador_blast_cli.py` | **CP-24**, CP-22, CP-23 |

### 8.2 Verificación de coherencia

| Verificación | ¿Se cumple? | Evidencia |
|---|---|---|
| Cada participante de las secuencias pertenece a un componente de la ficha | Sí | Tabla 3.4.2 y tabla de clases por componente (sección 4.1) |
| Cada mensaje entre componentes está en el catálogo de relaciones de la arquitectura | Sí | En la Aplicación Web (catálogo 7.2.2): `PantallaBusqueda → ControladorBusqueda` = Pantallas → Controlador de búsqueda (*Delega*); `PantallaBusqueda → ModeloBusqueda / ModeloResultados` = Pantallas → Modelos (*Muestra*, solo lectura); `ControladorBusqueda → ModeloBusqueda` (*Actualiza*); `ControladorBusqueda → ModeloResultados` (*Carga resultados*); `ControladorBusqueda → ClienteBackend` (*Envía*). Entre contenedores: `ClienteBackend → ControladorEjecucion` = Cliente del Backend → Backend (*Solicita*), que entra por Controladores y llega a Ejecución y persistencia (*Invoca*). En el Backend (catálogo 7.1.2): `ControladorEjecucion → AdaptadorBlast` (*Ejecuta*); `AdaptadorBlast → BLAST+` (*Invoca*); `ControladorEjecucion → RepositorioHistorial` (*Persiste*); `RepositorioHistorial → Base de datos` (*Lee y escribe*, SQL) |
| El diseño respeta las restricciones del estilo y de los patrones del contenedor | Sí | Cliente-servidor: el cliente inicia la comunicación y espera la respuesta. Capas: `dominio/` no importa nada de las otras carpetas y `aplicacion/` no importa `infraestructura/` ni `interfaz/` (6.1). MVC: los Modelos no conocen a la Vista (solo avisan a suscriptores anónimos); la Vista no modifica Modelos; solo el Controlador usa `ClienteBackend` |
| La táctica del escenario de calidad aparece como operación o mensaje | Sí | `EC-01`: `subprocess.run` dentro de `AdaptadorBlastCli.ejecutar`, en el hilo de cada solicitud. `EC-02`: `leer_salida` y `registrar_advertencia` |
| Cada entidad del diagrama de robustez está en el modelo de dominio (o se agregó) | Sí | `Busqueda` y `Alineamiento` están en el modelo de dominio. `ModeloBusqueda` y `ModeloResultados` son su representación en el cliente |
| Cada entidad que interviene según el paso 1 aparece en el diseño, o se explica por qué no | Sí | `Busqueda` y `Alineamiento` son clases. Las otras cinco intervienen como atributos de `Busqueda` (3.2) |
| El diagrama de clases coincide con el código | Sí | Obtenido con `pyreverse` y revisado; diferencias con el diseño previo en 4.2 |
| La medida del escenario tiene una prueba que la verifica | Sí | `EC-01` → CP-21 (cero cruces con cinco ejecuciones simultáneas); `EC-02` → CP-24 (campos obligatorios intactos y advertencia registrada) |
| Todo criterio de aceptación llega al menos a una prueba | Sí | Tabla 8.1 y cierre de 7.1 |
| Toda clase del diagrama aparece en alguna secuencia | Sí | Tabla de correspondencia de la sección 4.1 |

### 8.3 Actualizaciones a documentos anteriores

| Documento | Cambio | Motivo |
|---|---|---|
| [`modelo-dominio.md`](../requeriments/modelo-dominio.md) | Corrección de multiplicidades, nueva entidad `ProgramaBlast`, composiciones, relaciones del `Reporte` y ciclo de vida de la búsqueda (ver su *Registro de cambios*) | El modelo era previo a la partición de los casos de uso y a la arquitectura |
| [`historias-usuario.md`](../requeriments/historias-usuario.md) | CA-03 de `HU08_CU004_B`: la búsqueda se registra en el historial **antes** de presentar la tabla | Conflicto con la garantía mínima de `CU004` (3.1 y D4) |
| [`casos-de-uso.md`](../requeriments/casos-de-uso.md) | Flujo principal de `CU004`: el paso de persistencia pasa antes que el de presentación | Mismo motivo |
| [`architecture.md`](../architecture/architecture.md) | La secuencia y la configuración ya no se guardan antes de ejecutar; la ejecución deja de tener una "consulta de progreso" aparte; *Ejecución y persistencia* persiste antes de entregar los resultados; `DA-04` explica cómo se evita el cruce de resultados | Decisiones D1, D2, D3 y D4 de este diseño |
| [`architecture.md`](../architecture/architecture.md) | **Pendiente de decisión del grupo:** la tecnología del contenedor Aplicación Web figura como React; en el TP4 se implementó en Python (Tkinter) | Decisión D11. Si se adopta, actualizar las vistas de contenedores y de despliegue |

---

## 9. Glosario y bibliografía

### 9.1 Términos

| Término | Significado en este documento |
|---|---|
| Agregado | Grupo de entidades que se tratan como una unidad y se acceden a través de una entidad raíz. Aquí, `Busqueda` con sus alineamientos |
| Hit | Cada secuencia de la base de datos que BLAST+ encontró parecida a la query. En la salida de BLAST+ llega como datos; en el dominio se convierte en un `Alineamiento` |
| Historial | Conjunto de búsquedas ejecutadas con sus resultados crudos (almacén D2) |
| Polimorfismo | Que objetos de clases distintas respondan a la misma operación, cada uno a su manera. Aquí, las implementaciones de `RepositorioHistorial` responden a `guardar` cada una en su almacén |
| Subproceso | Proceso del sistema operativo que lanza el Backend para ejecutar un programa de BLAST+ |

Los términos del dominio (BLAST, BLAST+, query, E-value, FASTA, etc.) están en el [glosario del SRS](../requeriments/srs.md#10-glosario).

### 9.2 Bibliografía

- Valotto, V. *Diseño tridimensional de software*. 2025.
- Rosenberg, D. y Stephens, K. *Use Case Driven Object Modeling with UML: Theory and Practice*. Apress, 2007.
- Larman, C. *Applying UML and Patterns: An Introduction to Object-Oriented Analysis and Design and Iterative Development*. Prentice Hall.
- Gamma, E., Helm, R., Johnson, R. y Vlissides, J. *Design Patterns: Elements of Reusable Object-Oriented Software*. Addison-Wesley.
- Camacho, C. et al. *BLAST+ Command Line Applications User Manual*. NCBI.
