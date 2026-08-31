# LocalBlast_2026

## Integrantes
* Agustin Facundo Gaitan
* Wursten Augusto
* Farias Valentin

---

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

---

## 2. Documentación del Proyecto
Para consultar la Especificación de Requisitos de Software (SRS) completa, visión, casos de uso y escenarios de calidad, diríjase a:
👉 [`docs/requirements/srs.md`](docs/requirements/srs.md)

---

## 3. Modelo de Ciclo de Vida Específico
*(Agregar aquí la justificación de 3 a 5 líneas del modelo de ciclo de vida seleccionado para el proyecto).*
