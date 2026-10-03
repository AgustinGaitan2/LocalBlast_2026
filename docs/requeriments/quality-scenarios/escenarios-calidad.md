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
