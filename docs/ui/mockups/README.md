# Maquetado HTML — Primer ciclo de generación con IA

Esta carpeta contiene el maquetado HTML del flujo de navegación del Investigador/a, generado en el **primer ciclo** del proceso de maquetado asistido por IA. Cada archivo corresponde a una de las pantallas definidas en el flujo de navegación del perfil ([`../user-profiles/investigador.md`](../user-profiles/investigador.md), sección 3) y lleva en el nombre las historias de usuario que respalda.

## Archivos

| Archivo | Pantalla del flujo | HUs cubiertas |
|---|---|---|
| [`pantalla-01-carga-secuencia_HU01-HU02.html`](pantalla-01-carga-secuencia_HU01-HU02.html) | Nueva búsqueda — Secuencia query | `HU01_CU001_B`, `HU02_CU001_E1` |
| [`pantalla-02-configuracion-validacion_HU03-HU04-HU05-HU06-HU07.html`](pantalla-02-configuracion-validacion_HU03-HU04-HU05-HU06-HU07.html) | Nueva búsqueda — Configuración + validación | `HU03_CU002_B`, `HU04_CU002_A1`, `HU05_CU003_B`, `HU06_CU003_E1`, `HU07_CU003_E2` |
| [`pantalla-03-ejecucion_HU08-HU09-HU10.html`](pantalla-03-ejecucion_HU08-HU09-HU10.html) | Ejecución en progreso | `HU08_CU004_B`, `HU09_CU004_A1`, `HU10_CU004_E1` |
| [`pantalla-04-resultados-filtros-descarga_HU11-HU12-HU13-HU14.html`](pantalla-04-resultados-filtros-descarga_HU11-HU12-HU13-HU14.html) | Resultados · filtros · descarga | `HU11_CU005_B`, `HU12_CU006_B`, `HU13_CU007_B`, `HU14_CU007_A1` |

Las **14 HUs del catálogo** del TP1 que requieren interfaz quedan cubiertas por estos cuatro archivos. La pantalla de autenticación mencionada en el flujo del perfil **no se maqueta** en esta iteración: no hay HU que la respalde y el principio de diseño del grupo es *"si una pantalla no está respaldada por alguna HU, no se maqueta"*. El resto del flujo asume sesión ya iniciada.

Cada archivo HTML muestra apilados el **estado primario** (camino feliz) y los **estados alternativos y de excepción** cubiertos por sus HUs, cada uno con una etiqueta visible que indica a qué HU y a qué criterio de aceptación corresponde. Esta decisión se tomó para que la evaluación visual pueda recorrer todos los estados sin necesidad de interactuar. En la implementación final solo un estado será visible al mismo tiempo.

---