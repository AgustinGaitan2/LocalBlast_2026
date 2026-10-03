# Perfil de usuario — Investigador/a

> Perfil del **único actor principal del sistema con historias de usuario asociadas** (ver [SRS 2.2](../../requeriments/srs.md#22-actores-del-sistema)). El actor Administrador/a queda explícitamente fuera del alcance del proyecto ([SRS 1.4](../../requeriments/srs.md#14-fuera-del-alcance)) y no tiene historias de usuario, por lo que no se perfila. El actor secundario no humano BLAST+ no requiere perfil de usuario — no interactúa con la interfaz, es invocado por el backend.

## 1. Perfil de usuario

### Quién es

Persona que necesita correr alineamientos BLAST como parte de su labor académica o de investigación. Dentro de este único rol del sistema, el SRS ([2.1](../../requeriments/srs.md#21-stakeholders)) distingue dos subgrupos de stakeholders que pueden asumirlo:

- **Estudiantes de Grado y Posgrado**, que *"necesitan realizar alineamientos locales rápidos para trabajos prácticos o investigación sin perder tiempo en la configuración de entornos por terminal"*.
- **Investigadores y Docentes de Bioinformática / Biología Molecular**, que *"buscan una herramienta ágil e intuitiva para explorar resultados con filtros visuales personalizados que no están disponibles de forma nativa en la web tradicional"*.

Ambos subgrupos acceden a las mismas capacidades del sistema (todas las HU01 a HU14), por lo que son el mismo actor del sistema. Las diferencias entre ellos se reflejan en este perfil como **rangos de variación interna** (en nivel técnico, en frecuencia de uso, en qué subconjunto del flujo ejercen con más intensidad) más que como perfiles separados.

Rastreo: SRS 2.1 y 2.2 sobre los stakeholders que pueden asumir el rol de Investigador/a. La documentación del proyecto no describe ningún otro atributo demográfico del Investigador (edad, carrera específica, institución), por lo que este perfil no afirma nada en esos ejes.
