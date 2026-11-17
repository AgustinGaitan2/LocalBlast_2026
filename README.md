# LocalBlast_2026

## Integrantes
* Farias Valentin
* Gaitan Agustin Facundo
* Wursten Augusto

---
## Estructura del Repositorio

````
LocalBlast_2026/
├── .gitignore
├── README.md
├── requirements.txt
├── pyproject.toml              # configuración de pytest y de la cobertura
├── src/                        # código de HU08 (ver docs/design/diseno-detallado.md, sección 6)
│   ├── main.py                 # punto de arranque
│   ├── dominio/                # Busqueda, Alineamiento
│   ├── aplicacion/             # ControladorEjecucion e interfaces (AdaptadorBlast, RepositorioHistorial)
│   ├── infraestructura/        # BLAST+ real y simulado; historial en memoria y SQL
│   └── interfaz/               # ruta HTTP del Backend y Aplicación Web (MVC, Tkinter)
├── tests/                      # pruebas unitarias (pytest), misma estructura que src/
└── docs/
    ├── architecture/
    │   ├── architecture.md
    │   └── contexto-inicial.md
    ├── design/
    │   ├── diseno-detallado.md
    │   ├── cobertura.md
    │   └── generado/clases_pyreverse.mmd
    ├── requeriments/
    │   ├── casos-de-uso.md
    │   ├── historias-usuario.md
    │   ├── modelo-dominio.md
    │   ├── srs.md
    │   └── quality-scenarios/
    │       └── escenarios-calidad.md
    ├── ui/
    │   ├── mockups/
    │   │   ├── README.md
    │   │   ├── pantalla-01-carga-secuencia_HU01-HU02_inicial.html
    │   │   ├── pantalla-01-carga-secuencia_HU01-HU02_final.html
    │   │   ├── pantalla-02-configuracion-validacion_HU03-HU04-HU05-HU06-HU07_inicial.html
    │   │   ├── pantalla-02-configuracion-validacion_HU03-HU04-HU05-HU06-HU07_final.html
    │   │   ├── pantalla-03-ejecucion_HU08-HU09-HU10_inicial.html
    │   │   ├── pantalla-03-ejecucion_HU08-HU09-HU10_final.html
    │   │   ├── pantalla-04-resultados-filtros-descarga_HU08-HU11-HU12-HU13_inicial.html
    │   │   └── pantalla-04-resultados-filtros-descarga_HU08-HU11-HU12-HU13_final.html
    │   ├── heuristic-review/
    │   │   ├── README.md
    │   │   ├── pantalla-01-carga-secuencia_HU01-HU02.md
    │   │   ├── pantalla-02-configuracion-validacion_HU03-HU04-HU05-HU06-HU07.md
    │   │   ├── pantalla-03-ejecucion_HU08-HU09-HU10.md
    │   │   └── pantalla-04-resultados-filtros-descarga_HU08-HU11-HU12-HU13.md
    │   └── user-profiles/
    │       ├── README.md
    │       └── investigador.md
    └── uso-ia.md
````

## 1. Canvas de Descubrimiento (Síntesis)

### Problema
Actualmente, la realización de alineamientos locales de secuencias mediante BLAST presenta barreras de entrada significativas según el canal utilizado:
* **Línea de comandos (Consola):** Requiere recordar comandos complejos, sintaxis rigurosa y navegar por documentación extensa, lo que ralentiza el trabajo de usuarios sin perfil puramente bioinformático o técnico.
* **Interfaz Web Oficial (NCBI BLAST):** Aunque es accesible, carece de opciones avanzadas de filtrado directo e interactivo (como filtros instantáneos por % de identidad o cobertura posterior a la búsqueda) y resulta sobrecargada para consultas simples y rápidas.

### Stakeholders
* **Estudiantes de Grado y Posgrado:** Que necesitan realizar alineamientos locales rápidos para trabajos prácticos o investigación sin perder tiempo en la configuración de entornos por terminal.
* **Investigadores y Docentes de Bioinformática / Biología Molecular:** Que buscan una herramienta ágil e intuitiva para explorar resultados con filtros visuales personalizados que no están disponibles de forma nativa en la web tradicional.

### Alcance del Proyecto
* **Interfaz Gráfica Intuitiva:** Diseño web o desktop amigable para la introducción de secuencias query (FASTA/texto plano) y configuración simple de parámetros.
* **Integración con Motor BLAST:** Capacidad de enviar consultas y recibir resultados conectándose a NCBI (vía API/remoto) o ejecutables de BLAST local.
* **Filtros Avanzados y Personalizados:** Opciones de visualización y filtrado dinámico sobre la lista de resultados (ej. umbrales de identidad, cobertura, E-value, taxones).
* **Exportación de Resultados:** Descarga de resultados filtrados en formatos estándar (CSV, JSON, FASTA).

#### Fuera del Alcance (Out of Scope)
* Reescritura o modificación del algoritmo de alineamiento subyacente de BLAST.
* Implementación de herramientas de alineamiento múltiple (como ClustalW o Muscle) o modelado 3D de estructuras.
* Creación o administración de bases de datos genómicas complejas desde la aplicación.
* Administración de bases de datos locales desde la aplicación (rol Administrador). El diseño integral del sistema contempla un rol Administrador que dé de alta, actualice y baje bases de datos BLAST locales a partir de archivos FASTA. Esta capacidad se documenta a nivel de diagramas(DFD Nivel 0/1, modelo de dominio) para dejar la visión completa del producto, pero queda fuera del alcance de este cuatrimestre por restricciones de tiempo: no se profundiza como casos de uso ni historias de usuario, no tiene requerimientos funcionales asociados y no se implementará. Para las historias de usuario del modo local se asume que ya existe al menos una base de datos cargada en el catálogo.

---

## 2. Documentación del Proyecto
Para consultar la Especificación de Requisitos de Software (SRS) completa, visión, casos de uso y escenarios de calidad, diríjase a:
👉 [`docs/requeriments/srs.md`](docs/requeriments/srs.md)

Los escenarios de atributo de calidad (TP2 — Parte A), con su proceso de priorización y los 15 escenarios en formato ISO 25010, están en:
👉 [`docs/requeriments/quality-scenarios/escenarios-calidad.md`](docs/requeriments/quality-scenarios/escenarios-calidad.md)

Los perfiles de usuario, escenarios de uso y flujos de navegación que guían el maquetado de la interfaz están en:
👉 [`docs/ui/user-profiles/`](docs/ui/user-profiles/)

El maquetado HTML del flujo de navegación (un archivo por pantalla con sus HU en el nombre, en dos versiones por pantalla: `_inicial.html` del primer ciclo de generación con IA, y `_final.html` tras aplicar los hallazgos aceptados de la evaluación heurística) está en:
👉 [`docs/ui/mockups/`](docs/ui/mockups/)

La evaluación heurística de usabilidad, con los prompts enviados a la IA, su respuesta completa heurística por heurística, la revisión crítica del grupo sobre cada hallazgo y los ciclos de ajuste que terminaron en los `_final.html`, está en:
👉 [`docs/ui/heuristic-review/`](docs/ui/heuristic-review/)

El documento de Especificación de Arquitectura, con la elección de interoperabilidad como driver único, la derivación hasta estilo cliente-servidor, patrón de capas en el Backend y patrón MVC en la Aplicación Web, las decisiones de arquitectura (`DA-01` a `DA-08`), las vistas de contenedores, de componentes y de despliegue del modelo C4 con sus catálogos, y la trazabilidad escenario → táctica → estilo/patrón → decisión → elemento C4, está en:
👉 [`docs/architecture/architecture.md`](docs/architecture/architecture.md)

El diseño detallado de la historia `HU08_CU004_B · Ejecutar la búsqueda validada y ver sus resultados` (ficha y análisis tridimensional de la HU, diagrama de robustez, diagramas de secuencia, modelo de clases obtenido del código y su validación, justificación con GRASP, implementación, casos de prueba, complejidad ciclomática y trazabilidad hasta las pruebas) está en:
👉 [`docs/design/diseno-detallado.md`](docs/design/diseno-detallado.md)

El reporte de cobertura de las pruebas de HU08 y su análisis están en:
👉 [`docs/design/cobertura.md`](docs/design/cobertura.md)

El diagrama de contexto completo del sistema está en:
👉 [`docs/architecture/contexto-inicial.md`](docs/architecture/contexto-inicial.md)

---

## 3. Cómo instalar y ejecutar (TP4)

El TP4 implementa `HU08_CU004_B · Ejecutar la búsqueda validada y ver sus resultados`: un Backend en Python (FastAPI) con capas dominio / aplicación / infraestructura, y una Aplicación cliente MVC con interfaz gráfica mínima en Tkinter.

### Requisitos

- **Python 3.10 o posterior**. En Windows y macOS el instalador de python.org ya trae Tkinter; en Debian/Ubuntu: `sudo apt install python3-tk`.
- **BLAST+ 2.14 o posterior es opcional.** Si `blastn` no está en el `PATH`, el sistema usa un BLAST+ simulado con datos de demostración.

### Instalación (máquina limpia)

```bash
git clone https://github.com/AgustinGaitan2/LocalBlast_2026.git
cd LocalBlast_2026
python -m venv .venv
# Windows:  .venv\Scripts\activate
# Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
```

### Ejecutar la interfaz

```bash
python src/main.py
```

Abre la ventana con una secuencia de ejemplo y la base `base_demo` ya cargadas. Para recorrer la HU en la defensa:

1. **Camino principal:** presionar **Ejecutar búsqueda**. Aparece el indicador de progreso (el simulado tarda 2 s, y la ventana se puede seguir usando), y luego la tabla con hit, score, E-value, % identidad y % cobertura. La búsqueda queda guardada en `localblast.db`.
2. **Camino de rechazo:** cambiar la base de datos por `nt` (o cualquier otra) y ejecutar. Se muestra el mensaje de error de BLAST+, sin tabla, y no se guarda nada.

Opciones del punto de arranque (`python src/main.py --help`):

| Opción | Qué hace |
|---|---|
| `--historial memoria` | Historial en memoria, sin archivo |
| `--historial sqlite:///otra.db` | Historial en otro archivo SQLite (por defecto `sqlite:///localblast.db`, se crea solo) |
| `--historial postgresql://usuario:clave@host/localblast` | Historial en PostgreSQL (requiere `pip install psycopg2-binary`; las tablas se crean al arrancar) |
| `--adaptador cli` / `simulado` | Fuerza BLAST+ real o simulado (por defecto `auto`) |
| `--blast-bin RUTA` | Carpeta de los binarios de BLAST+ si no están en el `PATH` |
| `--demora 0.5` | Segundos que tarda el BLAST+ simulado |
| `backend` | Levanta solo el Backend en `http://127.0.0.1:8000` (documentación interactiva en `/docs`) |

Cambiar el historial o BLAST+ es cambiar una opción: `ControladorEjecucion` no se modifica (decisión D9 del diseño).

### Ejecutar las pruebas

```bash
python -m pytest                                          # 60 pruebas
python -m pytest --cov --cov-branch --cov-report=term-missing   # con cobertura de ramas
radon cc -s src                                           # complejidad ciclomática
```

---

## 4. Modelo de Ciclo de Vida Específico

El grupo se decanta por una **metodologia incremental con practicas agiles**. 

Esta elección se basa en que la herramienta posee características
funcionales intrínsecas que se pueden modularizar naturalmente.
Donde es posible la entrega de un modulo operativo cuyo desarrollo
es independiente de otros del mismo sistema (Por ejemplo, *procesar_secuencia*). 

Cada incremento añade una capacidad operativa completa y utilizable.

• Descartamos enfoques como *Cascada* dado que es un flujo estrictamente secuencial, donde no se avanza a la siguiente fase sin cerrar por completo al anterior, lo cual no es caracteristico de este proyecto dado que como bien mencionamos es posible separar responsabilidades. 

• Descartamos enfoques como *Modelo en V* porque es en parte una variacion del metodo en cascada. 

• Descartamos enfoques como *Espiral* dado que esta pensado para proyectos más grandes en donde un fallo implica consecuencias catastroficas y por eso
se deben llevar a cabo gestion de riesgos, en un proyecto como el presente añadir la complejidad de un modelo en espiral supera ampliamente la complejidad del software en si, lo que ralentiza el desarrollo.

• Descartamos enfoques como *iterativo* debido a que obligaria a rehacer todo
el sistema en cada ciclo, lo cual es ineficiente cuando **ya contamos con requisitos bien definidos**. Por lo que no seria necesario primero desarrollar un esqueleto basico del sistema para luego ir refinandolo, sino que al conocer bien los requisitos podemos simplemente construir un modulo dejandolo listo para produccion y luego construir el siguiente. 


