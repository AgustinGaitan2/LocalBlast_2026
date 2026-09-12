# Bitácora de uso de IA — TP1

Este documento registra el uso crítico de asistentes de IA generativa durante el TP1, según lo pedido por la cátedra: qué herramienta se usó, para qué tarea puntual, qué generó, qué se aceptó / modificó / descartó, y qué errores o imprecisiones se detectaron.

---

## Entrada 1 — Redacción inicial de casos de uso y HU a partir del canvas

- **Herramienta usada:** Claude, asistente de IA generativa basado en LLM.
- **Tarea concreta:** a partir del canvas de descubrimiento y de la lista preliminar de requerimientos funcionales que armamos como grupo, proponer un primer borrador de casos de uso (formato Cockburn) y de historias de usuario con criterios Given-When-Then.
- **Qué generó:**
  - Un CU-01 "Configurar y lanzar búsqueda BLAST" con flujo principal detallado, ~7 pasos, y una lista de slices secundarios A1/A2 nombrados.
  - Un primer intento de historias de usuario para el camino feliz y para el manejo de parámetros inválidos.
- **Qué aceptamos:**
  - La estructura Cockburn (actor / objetivo / precondición / flujo / postcondición / slices) del CU-01, porque encajaba con lo que pide el instructivo del TP1.
  - Los nombres de los slices secundarios como punto de partida.
- **Qué modificamos:**
  - **Alcance del CU:** el primer borrador de la IA mezclaba en un solo CU la carga de la secuencia, la elección del modo, la ejecución **y** la descarga de resultados. 
  - **Slices sobre modo remoto y modo local:** la IA los había pensado como CUs distintos ("CU-01a" y "CU-01b"). Los unificamos en el flujo principal con una bifurcación en el paso 2, porque el objetivo del actor es el mismo y el mecanismo se decide con un solo control ("elegir modo") no lo consideramos como casos de uso distintos.
- **Qué descartamos:**
  - Un slice "el usuario cambia de idioma en la interfaz" que la IA agregó. 
  - Un intento de la IA de sumar filtros por "score bruto" y "longitud del alineamiento" como criterios post-búsqueda esenciales. En el dominio real esos criterios existen pero los investigadores del grupo confirmaron que los cuatro que dejamos (identidad, cobertura, E-value observado, taxonomía) son los que efectivamente se usan; los otros se pueden sumar más adelante sin cambiar el modelo.
- **Errores / imprecisiones detectadas:**
  - La IA propuso, en un primer borrador, que el sistema **descargara automáticamente SwissProt** al dar de alta el sistema. Es un error: SwissProt se actualiza con frecuencia, tiene tamaño no trivial (~200 MB comprimida), y el laboratorio puede no querer que se cargue por defecto. Discutimos también la variante intermedia — permitir que el administrador indicara una URL desde la interfaz — y también la descartamos: en esta primera versión toda base de datos se carga por subida directa del archivo FASTA desde el equipo del administrador, incluso si el archivo proviene de una base de datos pública como SwissProt (el admin la descarga por fuera del sistema y sube el resultante). Simplifica el modelo, elimina una entidad externa del diagrama de contexto y evita meter en el sistema una descarga de red que no aporta al valor del TP.
  - La IA sugirió como **valor por defecto** del E-value máximo `1e-5` para todo BLAST, sin distinguir programa. En la práctica el default sano varía según el programa (`blastp` y `blastn` usan defaults distintos). Ajustamos el RF-04 para que diga "valores por defecto sensatos **según el programa BLAST correspondiente**", en vez de fijar el número.

## Entrada 2 — Revisión de la primera versión del DFD

- **Herramienta usada:** Claude, asistente de IA generativa basado en LLM.
- **Tarea concreta:** pegarle nuestro DFD Nivel 0 y Nivel 1 y pedirle que verificara el balanceo de flujos externos.
- **Qué generó:** una lista de siete flujos externos identificados y su presencia (sí / no) en cada nivel.
- **Qué aceptamos:** el chequeo de balanceo — nos ayudó a detectar que la primera versión del Nivel 1 tenía el flujo del administrador conectado por error al proceso P1 en lugar de a P3.
- **Qué modificamos:** reubicamos ese flujo en el diagrama antes de commitear.
- **Qué descartamos:** una sugerencia de la IA de "unir P1 y P2 en un solo proceso" para simplificar. La rechazamos porque justamente la separación entre P1 (ejecución) y P2 (filtrado post-búsqueda + entrega) refleja una decisión de dominio importante: los filtros post-búsqueda **no** vuelven a correr BLAST, y esa distinción se pierde si el DFD los mezcla.
- **Errores detectados:** ninguno de la IA en esta revisión, el error estaba en nuestro diagrama y la IA lo ayudó a detectar.
