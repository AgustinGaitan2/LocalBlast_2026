# LocalBlast_2026
## Integrantes
* Agustin Facundo Gaitan
* Wursten Augusto
* Farias Valentin

---
### Problema
Actualmente, la realización de alineamientos locales de secuencias mediante BLAST presenta barreras de entrada significativas según el canal utilizado:
* **Línea de comandos (Consola):** Requiere recordar comandos complejos, sintaxis rigurosa y navegar por documentación extensa, lo que ralentiza el trabajo de usuarios sin perfil puramente bioinformático o técnico.
* **Interfaz Web Oficial (NCBI BLAST):** Aunque es accesible, carece de opciones avanzadas de filtrado directo e interactivo (como filtros instantáneos por % de identidad o cobertura posterior a la búsqueda) y resulta sobrecargada para consultas simples y rápidas.

### StakeHolders
* **Estudiantes de Grado y Posgrado:** Que necesitan realizar alineamientos locales rápidos para trabajos prácticos o investigación sin perder tiempo en la configuración de entornos por terminal.
* **Investigadores y Docentes de Bioinformática / Biología Molecular:** Que buscan una herramienta ágil e intuitiva para explorar resultados con filtros visuales personalizados que no están disponibles de forma nativa en la web tradicional.

### Alcance del Proyecto

* **Interfaz Gráfica Intuitiva:** Diseño web o desktop amigable para la introducción de secuencias query (FASTA/texto plano) y configuración simple de parámetros.
* **Integración con Motor BLAST:** Capacidad de enviar consultas y recibir resultados conectándose a NCBI (vía API/remoto) o ejecutables de BLAST local.
* **Filtros Avanzados y Personalizados:** Opciones de visualización y filtrado dinámico sobre la lista de resultados (ej. umbrales de identidad, cobertura, E-value, taxones).
* **Exportación de Resultados:** Descarga de resultados filtrados en formatos estándar (CSV, JSON, FASTA).

### **Fuera del Alcance (Out of Scope)**
* Reescritura o modificación del algoritmo de alineamiento subyacente de BLAST.
* Implementación de herramientas de alineamiento múltiple (como ClustalW o Muscle) o modelado 3D de estructuras.
* Creación o administración de bases de datos genómicas complejas desde la aplicación.

%%{init: {'theme': 'base', 'themeVariables': { 'fontSize': '16px'}}}%%
graph TD
    %% Definición de los nodos con sus formas y textos
    A("<b>Usuario</b><br/>Envía secuencia")
    B(("<b>Sistema BLAST</b><br/><span style='color:#6a5acd'>amigable</span>"))
    C("<b>Motor BLAST</b><br/>NCBI / local")

    %% Conexiones con etiquetas de texto
    A <-->|Consulta y resultados| B
    B <-->|Alineamiento BLAST| C

    %% Definición de estilos para los nodos (formas, colores de fondo y bordes)
    %% style A (Rectángulo beige claro)
    style A fill:#f3f0e8,stroke:#9d9a90,stroke-width:1px,rx:8,ry:8,color:black
    
    %% style B (Círculo azul/púrpura pálido)
    style B fill:#eff1ff,stroke:#a4b4f0,stroke-width:1px,color:#6a5acd
    
    %% style C (Rectángulo verde menta pálido)
    style C fill:#e4f2eb,stroke:#77ae96,stroke-width:1px,rx:8,ry:8,color:#004d3e
    
    %% Configuración general para las conexiones y el texto
    %% LinkStyle para todas las líneas (más gruesas y color gris)
    linkStyle 0,1 stroke:#808080,stroke-width:2px,color:black;
