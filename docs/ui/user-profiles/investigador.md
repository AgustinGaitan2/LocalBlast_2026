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

