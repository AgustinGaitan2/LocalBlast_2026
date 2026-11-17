# Reporte de cobertura — HU08_CU004_B

Complemento de la [sección 7 del diseño detallado](diseno-detallado.md#7-pruebas).

## Cómo se genera

```bash
python -m pytest --cov --cov-branch --cov-report=term-missing
```

La configuración está en `pyproject.toml` (`[tool.coverage.run]`): se mide `src/` con cobertura de ramas y se excluyen tres archivos (ver "Qué no se mide").

## Reporte

Ejecución del 17/11/2026 en un entorno virtual nuevo, Python 3.13, pytest 9.1 y pytest-cov 7.1:

```text
Name                                                      Stmts   Miss Branch BrPart  Cover   Missing
-----------------------------------------------------------------------------------------------------
src/aplicacion/adaptador_blast.py                             8      0      0      0   100%
src/aplicacion/controlador_ejecucion.py                      16      0      0      0   100%
src/aplicacion/repositorio_historial.py                       5      0      0      0   100%
src/dominio/alineamiento.py                                  16      0      0      0   100%
src/dominio/busqueda.py                                      26      0      6      0   100%
src/infraestructura/adaptador_blast_cli.py                   65      0     20      0   100%
src/infraestructura/adaptador_blast_simulado.py              20      0      4      0   100%
src/infraestructura/repositorio_historial_en_memoria.py      14      0      0      0   100%
src/infraestructura/repositorio_historial_sql.py             21      0      2      0   100%
src/interfaz/cliente/cliente_backend.py                      26      0      0      0   100%
src/interfaz/cliente/controlador_busqueda.py                 27      0      0      0   100%
src/interfaz/cliente/modelo_busqueda.py                      33      0      0      0   100%
src/interfaz/cliente/modelo_resultados.py                    10      0      0      0   100%
src/interfaz/cliente/observable.py                            9      0      2      0   100%
src/interfaz/rutas.py                                        23      0      0      0   100%
-----------------------------------------------------------------------------------------------------
TOTAL                                                       319      0     34      0   100%
60 passed in 1.63s
```

(Se omiten las filas de los `__init__.py`, que están vacíos.)

## Análisis

**Qué no se mide y por qué.**

- `src/interfaz/cliente/pantalla_busqueda.py` (la Vista en Tkinter). La consigna pide no probar a través de la interfaz gráfica, y por diseño la Vista no tiene reglas: solo delega en `ControladorBusqueda` y dibuja lo que tienen los Modelos. Todo lo que decide qué se dibuja (estado, filas, mensaje de error) está en los Modelos y en el Controlador, que sí están cubiertos (CP-50 a CP-55). La Vista se verifica en la demostración: progreso, tabla y mensaje de error.
- `src/main.py`, el punto de arranque. Solo arma objetos según los argumentos de la línea de comandos; se verifica al ejecutar el sistema con cada combinación de `--adaptador` y `--historial`.
- `src/infraestructura/datos_demo.py`. Son datos, no comportamiento. Apareció con 0 % en el primer reporte y se excluyó por eso; no es un hueco de pruebas.

**Qué pruebas se agregaron al ver el reporte.** Ninguna por cobertura: el primer reporte ya daba 100 % de sentencias y ramas sobre el código medido, porque los casos de caja blanca se diseñaron antes desde la complejidad ciclomática (sección 7.2), con una prueba por camino. Lo que sí hizo el reporte fue confirmar que esa tabla no dejó ramas afuera. Las pruebas que agregó el análisis de caminos, y que los criterios de aceptación no pedían, son CP-33 (BLAST+ falla sin mensaje), CP-35 (tiempo máximo), CP-36 y CP-37 (programa o parámetro no admitidos), CP-58 (error HTTP sin cuerpo JSON) y CP-45 (búsqueda sin hits en la base SQL).

**Cobertura alta no es verificación.** El 100 % dice que todo se ejecutó, no que todo se verificó. Pruebas que pasan pero verifican poco, o que hay que mirar con cuidado:

- **CP-05** solo comprueba la conversión de tipos del constructor de `Alineamiento`; sería fácil que pase con un cálculo de porcentajes equivocado. Por eso los porcentajes tienen pruebas propias (CP-01 a CP-04) con valores calculados a mano.
- **CP-41 y CP-42** dependen del reloj (miden demoras con `time.perf_counter`). Verifican cotas holgadas para no ser inestables, pero en una máquina muy cargada podrían tardar más; no afectan la corrección del sistema, solo la del doble de prueba.
- **CP-21 (`EC-01`)** usa hilos reales con demoras distintas. Una prueba de concurrencia que pasa no demuestra que no haya carreras; lo que la hace significativa es que cada búsqueda tiene hits con nombres propios, de modo que cualquier cruce se detecta, y que el diseño no tiene estado compartido entre búsquedas (D3).
- **La lectura del XML** se prueba con salidas armadas a partir del formato de BLAST+ 2.14 (`tests/datos/`), no con una ejecución real. Antes de la defensa conviene reemplazar `salida_blastn_2_14.xml` por la salida de una corrida real con la base del laboratorio y volver a correr CP-22 a CP-24.
- **`RepositorioHistorialSql`** se prueba contra SQLite. Con PostgreSQL la clase es la misma, pero no hay una prueba automatizada contra esa base (sería una prueba de integración, opcional en este TP).
