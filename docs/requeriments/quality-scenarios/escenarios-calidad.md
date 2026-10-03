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

### 2.2 Atributos candidatos para la matriz de priorización

Quedan diez atributos para comparar entre sí:

| # | Subcaracterística | Característica (ISO 25010:2023) |
|---|---|---|
| 1 | Comportamiento temporal | Eficiencia de desempeño |
| 2 | Disponibilidad | Fiabilidad |
| 3 | Tolerancia a fallos | Fiabilidad |
| 4 | Capacidad de recuperación | Fiabilidad |
| 5 | Confidencialidad | Seguridad |
| 6 | Autenticidad | Seguridad |
| 7 | Operabilidad | Capacidad de interacción |
| 8 | Protección frente a errores del usuario | Capacidad de interacción |
| 9 | Interoperabilidad | Compatibilidad |
| 10 | Modularidad | Mantenibilidad |

La numeración de este listado se mantiene como índice de referencia para la matriz comparativa de la sección siguiente, en la que las columnas se referencian por su número para que la tabla no quede excesivamente ancha.

---

## 3. Matriz de priorización

**Convención.** En cada celda `(fila, columna)` se compara el atributo de la fila contra el atributo de la columna:

- `^` indica que **el atributo de la columna es más crítico** para LocalBlast.
- `<` indica que **el atributo de la fila es más crítico** para LocalBlast.
- La diagonal queda vacía (no se compara un atributo consigo mismo).
- Solo se completa el **triángulo superior** (la matriz es antisimétrica).

El puntaje final de cada atributo es la cantidad de comparaciones en que resultó ganador: se cuentan los `<` de su fila más los `^` de su columna (en las filas que están por encima de la diagonal).

### 3.1 Grilla comparativa 10×10

Las filas llevan el nombre completo del atributo; las columnas se identifican con el número de orden del listado de la sección 2.2.

| | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | **Puntaje** |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 1. Comportamiento temporal                         | — | `<` | `^` | `<` | `^` | `<` | `^` | `^` | `^` | `^` | **3** |
| 2. Disponibilidad                                  |   | — | `^` | `<` | `^` | `<` | `^` | `^` | `^` | `^` | **2** |
| 3. Tolerancia a fallos                             |   |   | — | `<` | `^` | `<` | `^` | `<` | `^` | `<` | **6** |
| 4. Capacidad de recuperación                       |   |   |   | — | `^` | `<` | `^` | `^` | `^` | `^` | **1** |
| 5. Confidencialidad                                |   |   |   |   | — | `<` | `^` | `<` | `^` | `<` | **7** |
| 6. Autenticidad                                    |   |   |   |   |   | — | `^` | `^` | `^` | `^` | **0** |
| 7. Operabilidad                                    |   |   |   |   |   |   | — | `<` | `^` | `<` | **8** |
| 8. Protección frente a errores del usuario         |   |   |   |   |   |   |   | — | `^` | `^` | **4** |
| 9. Interoperabilidad                               |   |   |   |   |   |   |   |   | — | `<` | **9** |
| 10. Modularidad                                    |   |   |   |   |   |   |   |   |   | — | **5** |

**Verificación.** Suma total de puntajes = 3 + 2 + 6 + 1 + 7 + 0 + 8 + 4 + 9 + 5 = **45**, que coincide con la cantidad total de comparaciones C(10,2) = 10·9/2 = 45. ✓


---


### 4.1 Ranking

Umbral elegido: **5 victorias**. Quedan los cinco atributos que superan ese umbral.

| Posición | Atributo (subcaracterística) | Puntaje | ¿Seleccionado? |
|:---:|---|:---:|:---:|
| 1 | Interoperabilidad | 9 | ✅ |
| 2 | Operabilidad | 8 | ✅ |
| 3 | Confidencialidad | 7 | ✅ |
| 4 | Tolerancia a fallos | 6 | ✅ |
| 5 | Modularidad | 5 | ✅ |
| 6 | Protección frente a errores del usuario | 4 | ❌ |
| 7 | Comportamiento temporal | 3 | ❌ |
| 8 | Disponibilidad | 2 | ❌ |
| 9 | Capacidad de recuperación | 1 | ❌ |
| 10 | Autenticidad | 0 | ❌ |

### 4.2 Síntesis de por qué estos cinco y no los otros

Los cinco atributos seleccionados cubren cuatro dimensiones distintas del sistema, todas críticas para LocalBlast:

- **Interoperabilidad** cubre la relación con el actor externo del que depende todo el sistema (BLAST+ y, a través suyo, NCBI). Sin ella no hay producto.
- **Operabilidad** cubre la relación con el actor humano principal (el investigador) y materializa la propuesta de valor frente a la línea de comandos.
- **Confidencialidad** cubre la protección de los datos sensibles que atraviesan el sistema. Las secuencias que un investigador puede cargar incluyen material biológico de origen humano, lo que las convierte en datos sensibles; la exposición de red (navegador ↔ servidor), el almacenamiento del historial y el acceso entre investigadores del mismo laboratorio son los tres frentes donde esta protección se juega.
- **Tolerancia a fallos** cubre la robustez ante los fallos externos previsibles (timeouts, rate limits, errores de NCBI reportados a través de BLAST+), que son frecuentes en el modo remoto.
- **Modularidad** cubre la evolución del sistema. El proyecto declara explícitamente un modelo de ciclo de vida incremental y deja fuera del alcance de este cuatrimestre el rol administrador, formatos adicionales y filtros adicionales, con la intención explícita de incorporarlos iterativamente. Un diseño no modular convierte esa intención en reescrituras.

Los que quedaron afuera no son irrelevantes, pero son de **menor prioridad relativa**: *Protección frente a errores del usuario* ya está ampliamente cubierta por los requerimientos funcionales de validación (sintáctica de la secuencia y semántica de la configuración); *Comportamiento temporal* importa pero queda subordinada a Operabilidad, que la contiene en términos de experiencia percibida; *Disponibilidad* y *Capacidad de recuperación* son moderadas en un lab que no exige 24/7 y tolera reintentos; y *Autenticidad* se materializa como mecanismo que apoya a Confidencialidad, no como atributo con exigencia propia independiente.

---

## 5. Escenarios de calidad

Para cada uno de los cinco atributos seleccionados se definen **dos escenarios**, ambos en entornos de sobrecarga, degradados o significativos, con los seis componentes de la plantilla ISO. Siguiendo la indicación de la guía del TP2, no se incluyen escenarios en condición normal: los escenarios buscan capturar las situaciones en las que el atributo realmente se pone en juego.

---

### 5.1 Interoperabilidad

**Característica / Subcaracterística:** Compatibilidad / Interoperabilidad.

**Justificación de criticidad del atributo.** LocalBlast *es*, por definición, una interfaz gráfica para BLAST+. Toda ejecución —local o remota— termina siendo una invocación al binario de BLAST+ con los argumentos adecuados y un parseo de su salida. La interoperabilidad con este sistema externo es condición de existencia del producto, y es el atributo con más victorias en la matriz comparativa (9 sobre 9).

**Escenario 1 — sobrecarga por concurrencia de invocaciones**

| Campo | Contenido |
|---|---|
| Fuente del estímulo | Varios investigadores del mismo laboratorio, trabajando simultáneamente |
| Estímulo | Lanzan hasta cinco búsquedas concurrentes contra el sistema, mezclando búsquedas locales (contra el catálogo del laboratorio) y remotas (contra NCBI a través de BLAST+) |
| Entorno | Sobrecarga — cinco invocaciones concurrentes a BLAST+ sobre el mismo servidor, cada una con parámetros, bases de datos y resultados distintos |
| Artefacto | Módulo de ejecución asíncrona del sistema, responsable de invocar BLAST+ como subproceso y de mantener la correspondencia entre cada subproceso y la sesión del investigador que lo originó |
| Respuesta | El sistema lanza cada búsqueda como un subproceso independiente de BLAST+, con su propio contexto de ejecución y su propio identificador; mantiene la asociación entre cada subproceso y la sesión del investigador correspondiente, y al terminar entrega los resultados exclusivamente a esa sesión, sin cruzarlos con los de otras búsquedas en curso |
| Medida de la respuesta | Cero cruces de resultados entre búsquedas concurrentes con hasta cinco búsquedas simultáneas |

*Criticidad:* un cruce de resultados entre investigadores sería un error silencioso: el investigador vería alineamientos ajenos como si fueran los suyos y los interpretaría en el contexto equivocado. Es el escenario típico de un laboratorio al final de la jornada, cuando varios investigadores lanzan búsquedas al mismo tiempo.

**Escenario 2 — degradado por cambio menor de versión de BLAST+**

| Campo | Contenido |
|---|---|
| Fuente del estímulo | BLAST+ como sistema externo |
| Estímulo | Devuelve una salida con cambios menores respecto a la versión soportada por el sistema: una columna adicional en la salida tabular, o un campo nuevo en la salida XML, tras una actualización menor del binario BLAST+ realizada por el administrador de sistemas sin coordinarla con el equipo de desarrollo |
| Entorno | Degradado — versión de BLAST+ posterior a la validada por el equipo de LocalBlast |
| Artefacto | Parser de la salida de BLAST+ dentro del módulo de ejecución, responsable de convertir el texto devuelto por el binario en la tabla de alineamientos que el investigador ve |
| Respuesta | El parser reconoce los campos conocidos y los extrae correctamente, detecta la presencia de campos adicionales no mapeados y los ignora sin corromper los campos conocidos, no aborta la ejecución, no bloquea la presentación de los resultados al investigador y registra una advertencia en el log del sistema para que el equipo de desarrollo pueda incorporar el nuevo campo en una iteración futura |
| Medida de la respuesta | El 100% de las búsquedas con salida de formato "casi conocido" (columnas adicionales no esperadas o campos XML nuevos) completan la presentación de resultados con los campos obligatorios (identificador del hit, score, E-value observado, porcentaje de identidad y porcentaje de cobertura) intactos; el 100% de esos casos quedan registrados en el log con la advertencia correspondiente |

*Criticidad:* BLAST+ es externo y lo actualiza el administrador de sistemas del laboratorio por decisiones ajenas al equipo de desarrollo de LocalBlast. Una actualización menor del motor no debería romper nuestro sistema. Es un escenario realista y recurrente en productos que envuelven herramientas que no controlan.

---

### 5.2 Operabilidad

**Característica / Subcaracterística:** Capacidad de interacción / Operabilidad.

**Justificación de criticidad del atributo.** La propuesta de valor explícita de LocalBlast frente a la línea de comandos de BLAST+ y frente a la interfaz web oficial de NCBI es ser *"ágil e intuitiva"* (ver canvas de descubrimiento en el README). Si la operabilidad falla, el investigador vuelve a la terminal y el producto pierde su razón de ser. Es el segundo atributo con más victorias en la matriz comparativa.

**Escenario 1 — sobrecarga por filtrado interactivo sobre muchos resultados**

| Campo | Contenido |
|---|---|
| Fuente del estímulo | Investigador trabajando con una búsqueda que devolvió un conjunto grande de alineamientos |
| Estímulo | Aplica sucesivamente cuatro filtros sobre la tabla de resultados (umbral de identidad, umbral de cobertura, umbral de E-value y filtro por taxonomía), modificando los umbrales varias veces por minuto para explorar interactivamente el conjunto |
| Entorno | Sobrecarga — tabla con más de 500 hits y ritmo rápido de ajuste de filtros |
| Artefacto | Módulo de filtrado posterior a la búsqueda y la interfaz de la tabla de resultados en el navegador |
| Respuesta | Cada cambio de filtro refresca la tabla en el momento sobre el conjunto crudo original (nunca sobre un resultado filtrado previo), los filtros aplicados quedan siempre visibles y editables, y el investigador puede combinarlos, aflojarlos, endurecerlos o quitarlos en cualquier orden sin tener que reiniciar nada y sin esperas significativas entre cambios |
| Medida de la respuesta | Cada actualización de la tabla ante un cambio de filtro se refleja en menos de **1 segundo** con tablas de hasta 500 hits; el estado de los filtros aplicados permanece visible y editable durante toda la sesión |

*Criticidad:* el filtrado interactivo posterior a la búsqueda es una de las dos capacidades que diferencian a LocalBlast de la interfaz web oficial de NCBI. Si no responde ágilmente en escenarios con muchos hits —que son los más interesantes desde el punto de vista biológico— el investigador vuelve a parsear la salida tabular a mano y pierde la ventaja del producto.

