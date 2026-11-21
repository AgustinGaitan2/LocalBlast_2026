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
├── requirements.txt              # dependencias del Backend (Python)
├── datos/
│   └── ejemplo/                  # query y base de proteínas sintéticas de demostración (FASTA)
├── scripts/
│   ├── crear_base_demo.sh        # construye la base BLAST de demostración (makeblastdb)
│   └── generar_datos_demo.py     # regenera los FASTA de demostración
├── src/
│   ├── backend/                  # Backend (Python / FastAPI), una carpeta por componente C4
│   │   ├── arranque.py           # punto de arranque: elige BLAST+ real o simulado y la persistencia
│   │   ├── controladores/        # Controladores (presentación): ruta HTTP
│   │   ├── ejecucion/            # Ejecución y persistencia (dominio): ControladorEjecucion, Busqueda, Alineamiento
│   │   ├── acceso_datos/         # Acceso a datos: RepositorioHistorial (SQLite y memoria), ConexionBD
│   │   └── adaptador_blast/      # Adaptador BLAST+: AdaptadorBlastCli y BLAST+ simulado
│   └── web/                      # Aplicación Web (React + Vite, patrón MVC)
│       └── src/
│           ├── pantallas/        # Vista: PantallaBusqueda
│           ├── controladores/    # ControladorBusqueda
│           ├── modelos/          # ModeloBusqueda, ModeloResultados
│           └── cliente/          # ClienteBackend
└── docs/
    ├── architecture/
    │   ├── architecture.md
    │   └── contexto-inicial.md
    ├── design/
    │   └── diseno-detallado.md
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

El diseño detallado de la historia `HU08_CU004_B · Ejecutar la búsqueda validada y ver sus resultados` (ficha y análisis tridimensional de la HU, diagrama de robustez, diagramas de secuencia, verificación de coherencia con la arquitectura y cambios que el diseño produjo en el modelo de dominio y en la arquitectura) está en:
👉 [`docs/design/diseno-detallado.md`](docs/design/diseno-detallado.md)

El diagrama de contexto completo del sistema está en:
👉 [`docs/architecture/contexto-inicial.md`](docs/architecture/contexto-inicial.md)

---

## 3. Cómo instalar y ejecutar

Lo implementado es la historia `HU08_CU004_B · Ejecutar la búsqueda validada y ver sus resultados`. La pantalla arranca con una búsqueda ya validada, porque la carga y la validación son otras historias.

### 3.1 Requisitos

* Python 3.10 o superior.
* Node.js 18 o superior, con npm.
* BLAST+ (opcional). Sin BLAST+, el sistema usa un BLAST+ simulado. Para usar el real: `sudo apt install ncbi-blast+`, o la instalación que ya tengan.

### 3.2 Instalación (una sola vez)

Desde la raíz del repositorio:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

cd src/web
npm install
npm run build        # compila la interfaz; el Backend la sirve en el puerto 8000
cd ../..

bash scripts/crear_base_demo.sh   # solo para BLAST+ real: crea datos/blastdb/proteinas_demo
```

### 3.3 Ejecutar la aplicación

Con el entorno virtual activado y desde la raíz del repositorio:

```bash
# BLAST+ simulado (no necesita BLAST+ instalado)
uvicorn backend.arranque:app --app-dir src --port 8000

# BLAST+ real de la máquina
LOCALBLAST_BLAST=real uvicorn backend.arranque:app --app-dir src --port 8000
```

Abrir <http://localhost:8000>.

* **Camino principal:** presionar *Ejecutar búsqueda*. Mientras corre se puede pasar a *Cómo leer los resultados* y volver; la ejecución no se interrumpe.
* **Camino de error:** abrir <http://localhost:8000/?ejemplo=base-inexistente>. BLAST+ no encuentra la base, se muestra su mensaje literal, no aparece ninguna tabla y no se guarda nada.

El historial queda en `datos/historial.sqlite3`. Para consultarlo: `sqlite3 datos/historial.sqlite3 "SELECT fecha, variante, base_datos FROM busqueda;"`.

**Modo desarrollo de la interfaz** (recarga al guardar cambios). Con el Backend corriendo en el puerto 8000, en otra terminal:

```bash
cd src/web && npm run dev     # abrir http://localhost:5173
```

### 3.4 Configuración

El Backend se configura con variables de entorno, todas opcionales:

| Variable | Valores | Para qué |
|---|---|---|
| `LOCALBLAST_BLAST` | `simulado` (por defecto) · `real` | BLAST+ simulado o el instalado en la máquina |
| `LOCALBLAST_BLAST_DIR` | carpeta | Dónde están `blastp`, `blastn`, etc., si no están en el `PATH` |
| `LOCALBLAST_LIMITE_SEGUNDOS` | número (por defecto 1800) | Tiempo máximo de una ejecución de BLAST+ |
| `LOCALBLAST_SIMULADO_DEMORA` | segundos (por defecto 3) | Cuánto tarda el simulado, para ver el indicador de progreso |
| `LOCALBLAST_SIMULADO_CAMPO_NUEVO` | `1` | El simulado agrega un campo desconocido a la salida (escenario `EC-02`; la advertencia aparece en la consola) |
| `LOCALBLAST_PERSISTENCIA` | `sqlite` (por defecto) · `memoria` | Historial en SQLite o en memoria; el controlador no cambia |
| `LOCALBLAST_BD` | archivo | Ubicación del archivo SQLite (por defecto `datos/historial.sqlite3`) |

**Usar otra secuencia u otra base:** ver la sección 3.5.

### 3.5 Probar otras secuencias con BLAST+ real

La pantalla no tiene un campo para pegar una secuencia: cargarla y validarla son otras historias de usuario (HU01 a HU07). Las búsquedas que se pueden ejecutar son las de `src/web/src/busquedas-validadas.json`, cada una con una clave que se elige desde la URL (`?ejemplo=<clave>`). Para probar otra secuencia se agrega ahí una entrada nueva.

> Con el BLAST+ **simulado** los resultados son siempre los de la búsqueda de demostración, sin importar la secuencia. Para probar secuencias propias hay que usar **BLAST+ real** (`LOCALBLAST_BLAST=real`).

#### Paso 1 · Convertir el FASTA en texto para el JSON

En el JSON la secuencia va en una sola línea, con `\n` en los saltos de línea. Este comando hace la conversión (desde la raíz del repositorio):

```bash
python3 -c "import json,sys; print(json.dumps(open(sys.argv[1]).read()))" mi_proteina.fasta
```

Imprime algo como `">mi_proteina Descripción\nMKTAYIAKQRQ...\n"`, comillas incluidas, listo para pegar en el campo `secuencia`.

#### Paso 2 · Agregar la búsqueda al JSON

Se agrega una entrada en `src/web/src/busquedas-validadas.json`, junto a `"demostracion"` y `"base-inexistente"`. Hay que respetar las comas entre entradas. Según dónde se quiera buscar:

**a) Contra una base de NCBI (modo remoto).** Necesita conexión a internet.

```json
"mi-prueba-ncbi": {
  "titulo": "Mi proteína contra SwissProt (NCBI)",
  "descripcion": "prueba remota con BLAST+ real",
  "configuracion": {
    "query_nombre": "mi_proteina.fasta",
    "secuencia": "<pegar acá lo que imprimió el paso 1>",
    "variante": "blastp",
    "modo": "remoto",
    "base_datos": "swissprot",
    "base_datos_nombre": "SwissProt (NCBI)",
    "parametros": { "evalue": 0.001, "matrix": "BLOSUM62" }
  }
}
```

**b) Contra una base local propia.** Primero se crea la base a partir de un FASTA con `makeblastdb`. Los encabezados del FASTA tienen que ser ASCII, sin acentos ni eñes.

```bash
makeblastdb -in mis_secuencias.fasta -dbtype prot -parse_seqids -out datos/blastdb/mi_base
```

```json
"mi-prueba-local": {
  "titulo": "Mi proteína contra mi base local",
  "descripcion": "prueba local con BLAST+ real",
  "configuracion": {
    "query_nombre": "mi_proteina.fasta",
    "secuencia": "<pegar acá lo que imprimió el paso 1>",
    "variante": "blastp",
    "modo": "local",
    "base_datos": "datos/blastdb/mi_base",
    "base_datos_nombre": "Mi base local",
    "parametros": { "evalue": 10, "matrix": "BLOSUM62" }
  }
}
```

Qué significa cada campo:

| Campo | Qué poner |
|---|---|
| `variante` | `blastp` (proteína contra proteínas), `blastn` (nucleótidos contra nucleótidos), `blastx`, `tblastn` o `tblastx`, de acuerdo con el tipo de la query y de la base |
| `modo` | `local` (una base de la máquina) o `remoto` (una base de NCBI; BLAST+ se invoca con `-remote`) |
| `base_datos` | En modo local, la ruta de la base sin extensión, relativa a la raíz del repositorio o absoluta. En modo remoto, el nombre de la base de NCBI: `swissprot`, `nr`, `pdb`, `refseq_protein` para proteínas; `nt` para nucleótidos |
| `parametros` | Opcionales: `evalue`, `word_size`, `matrix`, `gapopen`, `gapextend`, `max_target_seqs`. Tienen que corresponder a la variante; por ejemplo, `matrix` es solo para proteínas, así que con `blastn` no va |
| `query_nombre`, `query_longitud`, `query_unidad`, `base_datos_nombre` | Solo se muestran en la pantalla; no cambian la búsqueda |

#### Paso 3 · Compilar la interfaz y arrancar con BLAST+ real

El JSON queda incluido en la interfaz compilada, así que hay que volver a compilarla:

```bash
cd src/web && npm run build && cd ../..
LOCALBLAST_BLAST=real uvicorn backend.arranque:app --app-dir src --port 8000
```

Otra opción, que evita recompilar en cada cambio: dejar el Backend corriendo en una terminal y, en otra, `cd src/web && npm run dev`. Vite toma los cambios del JSON solo y la página queda en el puerto 5173.

#### Paso 4 · Ejecutar

Abrir `http://localhost:8000/?ejemplo=mi-prueba-ncbi` (o la clave que se haya usado; en el puerto 5173 si se usa el modo desarrollo) y presionar **Ejecutar búsqueda**. Las búsquedas disponibles también figuran en la sección *Cómo leer los resultados → Datos de demostración*.

Qué esperar:

- **Modo local:** con bases chicas el resultado aparece en segundos.
- **Modo remoto:** NCBI encola las búsquedas, así que puede tardar de uno a varios minutos. Mientras tanto se ve el indicador de progreso y se puede navegar. El límite es de 30 minutos; se cambia con `LOCALBLAST_LIMITE_SEGUNDOS`.
- **Si algo falla** (secuencia mal formada, parámetro que no corresponde a la variante, base inexistente, NCBI no responde): se muestra el mensaje literal de BLAST+, no aparece ninguna tabla y no se guarda nada.
- **Si sale bien:** la búsqueda queda en el historial, en `datos/historial.sqlite3`.

#### Alternativa sin tocar la interfaz: llamar a la API

Con el Backend corriendo, se puede enviar cualquier búsqueda directamente:

```bash
curl -X POST http://localhost:8000/api/busquedas/ejecucion \
  -H "Content-Type: application/json" \
  -d '{"secuencia": ">mi_proteina\nMKTAYIAKQRQ...", "variante": "blastp", "modo": "remoto", "base_datos": "swissprot", "parametros": {"evalue": 0.001}}'
```

La respuesta trae las filas de la tabla en JSON (`{"filas": [...]}`) o, si BLAST+ falló, `{"tipo": "ErrorBlast", "mensaje": "..."}`. La búsqueda se guarda en el historial igual que desde la interfaz.

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


