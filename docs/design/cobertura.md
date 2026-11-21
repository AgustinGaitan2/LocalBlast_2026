# Reporte de cobertura — HU08_CU004_B

Reporte de cobertura de las pruebas unitarias de `HU08_CU004_B` y su análisis. Los casos de prueba y la complejidad ciclomática están en la [sección 7 del diseño detallado](diseno-detallado.md#7-pruebas).

## 1. Cómo se genera

Desde la raíz del repositorio (ver la [sección 3.6 del README](../../README.md#36-ejecutar-las-pruebas)):

```bash
pytest --cov --cov-report=term-missing           # Backend: cobertura de líneas y de ramas
cd src/web && npm run test:cobertura              # Aplicación Web
```

**Qué se mide.**

- **Backend:** todo `src/backend` con cobertura de ramas (`branch = true` en `pyproject.toml`). Se excluye `arranque.py` (ver el análisis).
- **Aplicación Web:** los Modelos, el Controlador y el Cliente del Backend. No se mide la Vista (`pantallas/`) ni `main.jsx`, porque las pruebas unitarias no pasan por la interfaz gráfica.

## 2. Resultados

### 2.1 Backend (pytest + pytest-cov)

62 pruebas, todas pasan. Las dos de integración con BLAST+ real se ejecutaron porque BLAST+ y la base de demostración estaban disponibles; en una máquina sin ellos se omiten y pasan las otras 60.

```
Name                                                        Stmts   Miss Branch BrPart  Cover   Missing
-------------------------------------------------------------------------------------------------------
src/backend/__init__.py                                         0      0      0      0   100%
src/backend/acceso_datos/__init__.py                            0      0      0      0   100%
src/backend/acceso_datos/conexion_bd.py                        24      0      2      0   100%
src/backend/acceso_datos/repositorio_historial.py               3      0      0      0   100%
src/backend/acceso_datos/repositorio_historial_memoria.py      14      0      0      0   100%
src/backend/acceso_datos/repositorio_historial_sqlite.py       15      0      0      0   100%
src/backend/adaptador_blast/__init__.py                         0      0      0      0   100%
src/backend/adaptador_blast/adaptador_blast.py                 13      0      0      0   100%
src/backend/adaptador_blast/adaptador_blast_cli.py             72      0     16      0   100%
src/backend/adaptador_blast/blast_simulado.py                  19      0      4      0   100%
src/backend/controladores/__init__.py                           0      0      0      0   100%
src/backend/controladores/rutas.py                             26      0      2      0   100%
src/backend/ejecucion/__init__.py                               0      0      0      0   100%
src/backend/ejecucion/alineamiento.py                          21      0      4      0   100%
src/backend/ejecucion/busqueda.py                              31      0      2      0   100%
src/backend/ejecucion/controlador_ejecucion.py                 19      1      0      0    95%   21
-------------------------------------------------------------------------------------------------------
TOTAL                                                         257      1     30      0    99%
```

### 2.2 Aplicación Web (Vitest + cobertura v8)

18 pruebas, todas pasan.

```
-------------------|---------|----------|---------|---------|-------------------
File               | % Stmts | % Branch | % Funcs | % Lines | Uncovered Line #s 
-------------------|---------|----------|---------|---------|-------------------
All files          |     100 |      100 |     100 |     100 |                   
 cliente           |     100 |      100 |     100 |     100 |                   
  ...nteBackend.js |     100 |      100 |     100 |     100 |                   
 controladores     |     100 |      100 |     100 |     100 |                   
  ...orBusqueda.js |     100 |      100 |     100 |     100 |                   
 modelos           |     100 |      100 |     100 |     100 |                   
  ...loBusqueda.js |     100 |      100 |     100 |     100 |                   
  ...Observable.js |     100 |      100 |     100 |     100 |                   
  ...Resultados.js |     100 |      100 |     100 |     100 |                   
-------------------|---------|----------|---------|---------|-------------------
```

## 3. Análisis

### 3.1 Qué no quedó cubierto y por qué

| Qué | Por qué |
|---|---|
| Línea 21 de `controlador_ejecucion.py`, el cuerpo de `obtener_hora_actual()` | Es el reloj real que `ControladorEjecucion` usa por defecto. Las pruebas le pasan un reloj fijo, para no depender de la hora del sistema; por eso esa línea nunca se ejecuta en ellas. Se ejecuta en cada búsqueda de la aplicación, y la fecha guardada se ve en el historial. Una prueba que solo llame a `obtener_hora_actual()` no verificaría ningún comportamiento de la HU. |
| `src/backend/arranque.py` (excluido de la medición) | Es el punto de arranque: lee variables de entorno y arma los objetos. No tiene reglas de la HU. Se verifica al iniciar la aplicación: la consola informa qué BLAST+ y qué persistencia se usan. |
| La Vista (`PantallaBusqueda.jsx`, `formato.js`) y `main.jsx` (no medidos) | Las pruebas unitarias no pasan por la interfaz gráfica. La Vista no tiene reglas del negocio: dibuja lo que tienen los Modelos. Se verificó recorriendo la interfaz en el navegador (camino principal, navegación durante la ejecución y camino de error). |
| La concurrencia a nivel HTTP | La prueba de `EC-01` lanza las cinco búsquedas sobre `ControladorEjecucion` desde cinco hilos, que es lo que hace FastAPI con cada solicitud. Que FastAPI use un hilo por solicitud es una característica del framework y se verificó aparte: cinco solicitudes HTTP de 2 segundos terminaron en 2,1 segundos. |

### 3.2 Pruebas agregadas al ver el reporte y al revisar los caminos

| Prueba | Qué se vio | Qué se agregó |
|---|---|---|
| `CP-58` | El reporte de la Aplicación Web marcaba sin cubrir `ModeloBusqueda.obtener_fin()`: la hora que muestra el chip "Guardado en el historial" no se verificaba | Una prueba con el reloj controlado que comprueba que la hora de fin es la del momento en que terminó la ejecución, bien o con error |
| `CP-36` (caso "vacía") y `CP-39` (caso "sin carpeta") | Al armar la tabla de complejidad ciclomática faltaba un camino independiente en `Busqueda.longitud_query` y otro en el `__call__` del simulado. El reporte de ramas no los marcaba: la cobertura de ramas no exige recorrer todos los caminos | Un caso más en cada prueba parametrizada |

### 3.3 Pruebas que pasaban pero verificaban poco

Una cobertura del 100 % solo dice que el código se ejecutó, no que se haya verificado. Para comprobar que las pruebas verifican comportamiento real, se introdujeron a propósito seis errores en las reglas de la HU (*mutantes*) y se corrió la suite con cada uno:

| Error introducido | ¿Alguna prueba falla? |
|---|---|
| R1: % identidad dividido por la longitud de la query en vez de la del alineamiento | **No, en la primera versión.** Sí después de corregir `CP-04` |
| R1: cobertura sin valor absoluto (tramos invertidos de `blastx`) | Sí (`CP-05`) |
| R5: no se advierten los campos desconocidos | Sí (`CP-19`) |
| CA-03: no se guarda la búsqueda en el historial | Sí (`CP-08`, `CP-09`) |
| R4: se ignora el código de salida de BLAST+ | Sí (`CP-24`) |
| R4 (Aplicación Web): el error no se registra en el Modelo | Sí (`CP-14`) |

**El caso que se corrigió.** La primera versión de `CP-04` usaba un alineamiento de 420 residuos sobre una query de 420. Con longitudes iguales, dividir por cualquiera de las dos da el mismo resultado, así que la prueba pasaba aunque la fórmula estuviera mal. Era una prueba que pasaba y cubría la línea, pero no verificaba la regla. Ahora el alineamiento mide 300 sobre una query de 420, y el error introducido hace fallar la prueba.

### 3.4 Conclusión

- **Cobertura:** el Backend tiene 100 % de ramas y 99 % de líneas; la Aplicación Web, 100 % en las cuatro medidas. Lo único sin cubrir es el reloj real, a propósito.
- **Caminos:** cada camino independiente de las operaciones de la HU tiene su prueba (tabla 7.3 del diseño detallado).
- **Verificación:** los seis errores introducidos en las reglas principales son detectados por al menos una prueba.
