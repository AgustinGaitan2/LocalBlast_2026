# Escenarios de Atributo de Calidad — LocalBlast

Este documento contiene la selección, priorización y especificación de los atributos de calidad críticos para **LocalBlast**, junto con sus escenarios de calidad (seis componentes cada uno). Es parte del TP2 — Parte A y se apoya en el proyecto del TP1 (visión, alcance y requerimientos) para dar contexto a cada escenario.

**Taxonomía utilizada.** Las subcaracterísticas se toman del modelo de calidad del producto de la **ISO/IEC 25010:2023** (ver Anexo A de la guía del TP2). Para cada atributo elegido se declara explícitamente la característica y la subcaracterística correspondientes.

---

## 1. Metodología

Aplicamos el método de priorización por matriz comparativa visto en clase, con los siguientes pasos:

1. **Filtrado inicial.** Partimos del catálogo completo de subcaracterísticas de la ISO/IEC 25010:2023 y descartamos las que no aportan valor significativo al tipo de sistema que estamos desarrollando (una interfaz gráfica web para BLAST+, de ámbito de un laboratorio, con pocos usuarios concurrentes, que opera sobre secuencias biológicas potencialmente sensibles, y que está pensada para evolucionar iterativamente). Quedamos con **diez atributos candidatos**.
2. **Comparación por pares.** Construimos una matriz triangular 10×10 donde comparamos cada atributo con cada uno de los otros, respondiendo la pregunta: *¿cuál es más crítico para LocalBlast?*. Usamos la notación `^` / `<` descrita en la sección 3.
3. **Conteo y umbral.** Para cada atributo contamos cuántas veces resultó ganador en las comparaciones. Fijamos un umbral de **5 victorias** y nos quedamos con los **cinco atributos** por encima de ese umbral.
4. **Especificación de escenarios.** Para cada atributo elegido redactamos **dos escenarios**, ambos en entornos de sobrecarga, degradados o significativos, con los seis componentes de la plantilla ISO: fuente del estímulo, estímulo, artefacto, entorno, respuesta y medida de la respuesta. Siguiendo la indicación de la guía del TP2 (sección 3.1), no incluimos escenarios en condición normal: los escenarios deben capturar las situaciones en las que el atributo realmente se pone en juego.

---

## 2. Filtrado inicial de atributos

### 2.1 Atributos descartados

La ISO/IEC 25010:2023 define ocho características con sus subcaracterísticas (unas 30 en total). Para LocalBlast descartamos las siguientes antes de la matriz comparativa, porque **no aportan valor significativo al alcance definido del proyecto**:

| Subcaracterística | Motivo del descarte |
|---|---|
| **Completitud / Corrección / Pertinencia funcional** (Adecuación funcional) | Son requerimientos de "correctitud funcional" que ya quedan cubiertos por los requerimientos funcionales del TP1. No se tratan como atributos no funcionales a especificar aparte. |
| **Utilización de recursos** (Eficiencia de desempeño) | El cuello de botella real de performance es BLAST+ (externo), no nuestro código. No tenemos una restricción fuerte de CPU/RAM/disco impuesta por el laboratorio. |
| **Capacidad** (Eficiencia de desempeño) | El laboratorio tiene pocos usuarios concurrentes (menos de diez). Los límites máximos no son el driver de arquitectura. |
| **Ausencia de fallos** (Fiabilidad) | Queda cubierta implícitamente por *Tolerancia a fallos* y por la validación semántica de la configuración antes de ejecutar BLAST+. |
| **No repudio** (Seguridad) | Típico de dominios financiero/legal. No hay requerimiento del laboratorio de poder probar formalmente que un investigador lanzó cierta búsqueda. |
| **Responsabilidad / accountability** (Seguridad) | Mismo motivo que no repudio. El historial sirve al usuario, no como mecanismo de auditoría formal. |
| **Resistencia** (Seguridad) | Pensada para sistemas bajo ataque sostenido. LocalBlast es un sistema interno de laboratorio, sin exposición pública relevante. |
| **Reconocibilidad de la adecuación** (Capacidad de interacción) | Más propia de productos de catálogo público, no de una herramienta interna cuyos usuarios ya conocen por qué la usan. |
| **Capacidad de aprendizaje** (Capacidad de interacción) | Importante, pero queda subsumida por *Operabilidad* en nuestro caso: los usuarios ya conocen BLAST; lo que hay que aprender es la interfaz. |
| **Compromiso del usuario** (Capacidad de interacción) | Pensada para productos de consumo. Los investigadores no vuelven a LocalBlast por "engagement", sino para hacer su trabajo. |
| **Inclusividad / Asistencia al usuario / Autodescriptividad** (Capacidad de interacción) | Importantes en general; no son los drivers principales para una herramienta interna de laboratorio con usuarios de perfil técnico. |
| **Coexistencia** (Compatibilidad) | LocalBlast corre en un servidor dedicado del laboratorio. No convive con otros sistemas que compitan por sus recursos. |
| **Reusabilidad / Analizabilidad / Capacidad de prueba** (Mantenibilidad) | Importantes para el equipo, pero quedan cubiertas por buenas prácticas internas; no son requerimientos exigidos por el usuario final ni condicionan la arquitectura al nivel que lo hace *Modularidad*. |
| **Modificabilidad** (Mantenibilidad) | Queda subsumida por *Modularidad*: la capacidad de modificar sin romper se materializa, en nuestro caso, a través de la separación en módulos independientes. |
| **Adaptabilidad / Instalabilidad / Reemplazabilidad** (Flexibilidad) | El entorno de despliegue está definido (servidor del laboratorio, BLAST+ instalado por el administrador de sistemas). No hay requerimiento de portabilidad entre entornos ni de reemplazo. |
| **Escalabilidad** (Flexibilidad) | El dimensionamiento es conocido (una decena de investigadores). Crecimientos mayores están fuera del horizonte del proyecto. |
