# Perfil de usuario — Investigador/a

> Perfil del **único actor principal del sistema con historias de usuario asociadas** (ver [SRS 2.2](../../requeriments/srs.md#22-actores-del-sistema)). El actor Administrador/a queda explícitamente fuera del alcance del proyecto ([SRS 1.4](../../requeriments/srs.md#14-fuera-del-alcance)) y no tiene historias de usuario, por lo que no se perfila. El actor secundario no humano BLAST+ no requiere perfil de usuario — no interactúa con la interfaz, es invocado por el backend.

## 1. Perfil de usuario

### Quién es

Persona que necesita correr alineamientos BLAST como parte de su labor académica o de investigación. Dentro de este único rol del sistema, el SRS ([2.1](../../requeriments/srs.md#21-stakeholders)) distingue dos subgrupos de stakeholders que pueden asumirlo:

- **Estudiantes de Grado y Posgrado**, que *"necesitan realizar alineamientos locales rápidos para trabajos prácticos o investigación sin perder tiempo en la configuración de entornos por terminal"*.
- **Investigadores y Docentes de Bioinformática / Biología Molecular**, que *"buscan una herramienta ágil e intuitiva para explorar resultados con filtros visuales personalizados que no están disponibles de forma nativa en la web tradicional"*.

Ambos subgrupos acceden a las mismas capacidades del sistema (todas las HU01 a HU14), por lo que son el mismo actor del sistema. Las diferencias entre ellos se reflejan en este perfil como **rangos de variación interna** (en nivel técnico, en frecuencia de uso, en qué subconjunto del flujo ejercen con más intensidad) más que como perfiles separados.

Rastreo: SRS 2.1 y 2.2 sobre los stakeholders que pueden asumir el rol de Investigador/a. La documentación del proyecto no describe ningún otro atributo demográfico del Investigador (edad, carrera específica, institución), por lo que este perfil no afirma nada en esos ejes.

### Objetivo que persigue con el sistema

Correr alineamientos BLAST sobre una secuencia de interés, **sin pelearse con la línea de comandos de BLAST+**, con la posibilidad de usar tanto bases de datos remotas (NCBI) como bases propias del laboratorio, de **explorar los resultados interactivamente** con filtros que la web oficial no ofrece y de **llevarse el resultado** en un formato utilizable fuera del sistema.

Qué parte del objetivo pesa más depende del contexto concreto del Investigador:

- Para un uso académico puntual (p. ej. identificar una secuencia para un trabajo puntual), el valor se cierra con *"ver un resultado útil en pantalla"* — HUs del P1.
- Para un uso de investigación sostenida, el valor se cierra con *"explorar con filtros y descargar el subconjunto relevante"* — HUs del P1 más las HUs del P2.

### Contexto de uso

- **Lugar.** Entornos académicos o de laboratorio: aula de la facultad, sala de cómputos, box del grupo de investigación, laboratorio del grupo, o incluso la propia casa durante el estudio o trabajo remoto. **Supuesto del grupo:** el SRS no fija ubicación concreta, se infiere de las menciones a *"cursada"* y *"laboratorio"* en SRS 2.1.
- **Dispositivo.** Laptop o PC de escritorio con un navegador moderno. **Supuesto del grupo:** el SRS fija *"Interfaz web"* en el alcance ([SRS §1.3](../../requeriments/srs.md#13-dentro-del-alcance)) pero no describe el dispositivo concreto. El sistema no está pensado para uso cómodo en celular.
- **Urgencia.** Variable según el contexto del Investigador: desde media-alta cuando el trabajo responde a una fecha de entrega (informe, deadline académico) hasta baja cuando el trabajo es exploratorio y sostenido. **Supuesto del grupo:** el SRS habla de *"alineamientos rápidos"* como necesidad en 2.1 pero no fija niveles concretos de urgencia.
- **Frecuencia de uso.** También variable: desde uso por rachas durante entregas académicas puntuales hasta uso cotidiano durante proyectos de investigación activos (**Supuesto del grupo.**)

### Nivel de conocimiento técnico

El SRS caracteriza al Investigador con un **rango** de conocimiento técnico, no con un valor único:

- **Dominio (biología molecular / bioinformática).** De básico-intermedio a alto. En el extremo inferior, un estudiante entiende qué es una secuencia FASTA y la idea general de BLAST pero puede dudar frente a elegir programa (`blastn` vs. `blastx`) o fijar un E-value. En el extremo superior, un investigador sénior distingue perfectamente los programas, elige matriz de sustitución, interpreta E-values de memoria y tiene criterios formados sobre umbrales razonables. Rastreo: SRS 1.1 ubica a *"usuarios sin perfil puramente bioinformático o técnico"* como un extremo del público objetivo, y SRS 2.1 ubica a *"Investigadores y Docentes de Bioinformática / Biología Molecular"* como el otro.
- **Herramientas.** Todos los Investigadores manejan el navegador y los archivos de su computadora con soltura. La familiaridad con la terminal, con la instalación de BLAST+, con los nombres de flags y con el parseo de la salida varía fuertemente, desde nula (estudiante) hasta cómoda pero fastidiosa (sénior que la usó y prefiere evitarla). Rastreo: SRS 1.1 (fricción de la Interfaz de Línea de Comandos).
- **Lectura de documentación técnica.** Todos pueden leerla si no les queda otra, pero todos prefieren evitarla, nadie quiere revisar la documentación de BLAST+ para cada búsqueda. Rastreo: README 1 — *"recordar comandos complejos, sintaxis rigurosa y navegar por documentación extensa"*.

**Implicancia para el maquetado.** La interfaz debe ser accesible para el extremo inferior del rango (defaults sensatos, mensajes de error claros, nada que exija conocer flags) sin sacarle control al extremo superior (poder ajustar parámetros manualmente, poder usar bases locales del grupo, poder descargar en formatos como XML o tabular BLAST que un script existente ya sabe leer). Esta tensión se resuelve al definir las pantallas concretas.

### Limitaciones y frustraciones que condicionan su uso

- **Riesgo de errores en la configuración.** El extremo menos técnico puede elegir un programa BLAST incompatible con su query (p. ej. `blastp` sobre ADN) o poner un parámetro fuera de rango sin darse cuenta; necesita mensajes de error diagnósticos, no genéricos. Rastreo: existencia explícita de `HU02_CU001_E1` (secuencia inválida), `HU06_CU003_E1` (parámetros fuera de rango), `HU07_CU003_E2` (combinación incompatible).
- **BLAST+ y NCBI fallan seguido en la práctica.** Timeouts, rate limits, errores remotos. El Investigador necesita que, cuando algo falla, la interfaz le muestre el mensaje literal, para distinguir un problema de red temporal de uno más grave. Rastreo: `HU10_CU004_E1`.
- **Base local en estado inconsistente.** Si la base del laboratorio que planea usar está actualizándose o con índices corruptos, no quiere que el sistema le sustituya en silencio por otra ni que lo pase a modo remoto solo. Rastreo: `HU04_CU002_A1`.

## 2. Escenario de uso

**Historia de usuario de referencia.** El escenario se construye alrededor de **`HU13_CU007_B` · *Descargar los alineamientos actualmente visibles en un formato***. Se elige esta HU como terminal porque es la que cierra el ciclo completo de valor del Investigador: una vez descargado el subconjunto que importa, puede llevarse el trabajo fuera del sistema. La narración incluye naturalmente las HUs encadenadas necesarias para llegar hasta allí: `HU01_CU001_B` (carga de la secuencia), `HU03_CU002_B` (configuración), `HU05_CU003_B` (validación semántica), `HU08_CU004_B` (ejecución), `HU11_CU005_B` (tabla y persistencia automática) y `HU12_CU006_B` (filtros post-búsqueda). Esta elección cubre el camino feliz completo del sistema (los dos procesos profundizados, P1 y P2) y por lo tanto da el mejor insumo al maquetado posterior.

### Narración (camino feliz)

Un Investigador abre LocalBlast desde su navegador y se autentica con su usuario. En la pantalla de nueva búsqueda sube la secuencia que quiere alinear: un archivo FASTA bien formado con un único registro de proteína. El sistema le confirma la carga y le muestra que infirió alfabeto *"proteína"*.

Pasa a la configuración. Elige modo (local o remoto, según necesite usar una base del laboratorio o una pública de NCBI), selecciona del catálogo la base correspondiente, elige el programa BLAST adecuado para su query (`blastp`, en este caso) y revisa los parámetros pre-búsqueda. Si está cómodo con los defaults, los deja; si no, los ajusta a los valores con los que trabaja. Presiona *"Validar búsqueda"*. El sistema verifica semánticamente la configuración (alfabeto compatible con el programa, rangos de parámetros, combinación programa/query/base coherente) y le da el visto bueno. Se habilita el botón *"Ejecutar búsqueda"*, lo presiona.

La búsqueda corre en segundo plano. La interfaz muestra un indicador de progreso visible y le permite seguir navegando por la aplicación sin interrumpir la ejecución; también le ofrece la opción de cancelarla si cambia de idea. Al terminar, los resultados aparecen en una tabla con las columnas mínimas (identificador del hit, score, E-value observado, % de identidad, % de cobertura), y un cartel discreto le confirma que la búsqueda quedó guardada en el historial automáticamente.

Ahora el Investigador quiere refinar la vista para quedarse con lo relevante. Abre el panel de filtros post-búsqueda y pone *identidad ≥ 80%* y *cobertura ≥ 60%*. La tabla se re-filtra inmediatamente, sin volver a correr BLAST. Mira el subconjunto y decide ajustar: afloja la cobertura a *≥ 50%*. La tabla se re-filtra otra vez contra el conjunto crudo original (no contra el filtro anterior), y aparecen algunos hits adicionales. Satisfecho, elige formato **CSV** y presiona *"Descargar"*. El archivo que recibe contiene los hits visibles —los que superan los filtros vigentes— con las columnas mínimas y una sección de metadatos: parámetros pre-búsqueda, base utilizada, timestamp y filtros aplicados.

Más tarde vuelve al historial y confirma algo que le importa: la entrada guardada sigue conteniendo el conjunto crudo completo (no la lista filtrada), por lo que puede volver y probar umbrales distintos sin relanzar BLAST+.

### Variantes realistas

El Investigador se encuentra, de forma recurrente, con dos clases de situaciones que el camino feliz no cubre y que la interfaz debe sostener:

- **Secuencia con formato inválido (`HU02_CU001_E1`).** Al pegar una secuencia con un carácter fuera del alfabeto ,típicamente un número de posición o un símbolo que quedó al copiar, el sistema no la marca como cargada y muestra un mensaje claro que indica cuál es el carácter inválido y en qué posición aparece. El Investigador corrige y continúa.
- **Base local no disponible (`HU04_CU002_A1`).** Al elegir una base local que está actualizándose, el sistema lo informa explícitamente (*"la base '\<nombre\>' está siendo actualizada y no puede usarse"*) y lo devuelve al paso de selección con la lista refrescada, **sin** sustituir en silencio por otra ni pasar a modo remoto por su cuenta. El Investigador decide si espera o elige otra base.
