# Diagrama de clases del Backend generado con pyreverse

Salida de `pyreverse` (pylint) sobre `src/backend`, tal como la genera la herramienta. Solo se quitaron tres clases de librerías de terceros (`BaseModel` y `ConfigDict` de pydantic, `TypedDict` de typing), que no son parte del diseño. El diagrama limpio y revisado está en la [sección 4 del diseño detallado](diseno-detallado.md#4-modelo-de-clases).

Comando, desde la raíz del repositorio (requiere `pip install pylint`):

```bash
PYTHONPATH=src pyreverse -o mmd -p LocalBlast --filter-mode ALL -a 0 -s 0 src/backend
```

```mermaid
classDiagram
  class AdaptadorBlast {
    ejecutar(variante: str, secuencia: str, base_datos: str, remota: bool, parametros: dict)* list[Hit]
  }
  class AdaptadorBlastCli {
    _directorio_blast : Path | None
    _directorio_trabajo : Path | None
    _ejecutor : Callable
    _limite_segundos : float | None
    \_\_init\_\_(ejecutor: EjecutorComando, directorio_blast: Path | None, directorio_trabajo: Path | None, limite_segundos: float | None) None
    _armar_comando(variante: str, base_datos: str, remota: bool, parametros: dict) list[str]
    _leer_hit(hit: ET.Element) Hit
    ejecutar(variante: str, secuencia: str, base_datos: str, remota: bool, parametros: dict) list[Hit]
    leer_salida(salida_xml: str) list[Hit]
    registrar_advertencia(campos: list[str]) None
  }
  class Alineamiento {
    descripcion : str
    evalue : float
    id_hit : str
    identidades : int
    longitud_alineamiento : int
    longitud_query : int
    query_desde : int
    query_hasta : int
    score : float
    \_\_init\_\_(hit: Hit, longitud_query: int) None
    calcular_porcentaje_cobertura() float
    calcular_porcentaje_identidad() float
  }
  class BlastSimulado {
    _campo_nuevo : bool
    _demora_segundos : float
    _salida
    \_\_call\_\_(comando: list[str], entrada: str, directorio: Path | None, limite_segundos: float | None) ResultadoComando
    \_\_init\_\_(demora_segundos: float, campo_nuevo: bool, salida_grabada: Path) None
  }
  class Busqueda {
    _alineamientos : list[Alineamiento]
    _resultados_registrados : bool
    alineamientos : tuple[Alineamiento, ...]
    base_datos : str
    es_remota : bool
    fecha : datetime
    longitud_query : int
    modo : str
    parametros : dict
    secuencia : str
    variante : str
    \_\_init\_\_(configuracion: dict, fecha: datetime) None
    armar_tabla_resultados() list[dict]
    registrar_resultados(hits: list[Hit]) None
  }
  class ConexionBD {
    _limite_espera_segundos : float
    _ruta : Path
    \_\_init\_\_(ruta: Path, limite_espera_segundos: float) None
    _abrir_conexion() sqlite3.Connection
    ejecutar_transaccion(registro: list[Sentencia]) None
  }
  class ControladorEjecucion {
    _adaptador
    _reloj : Callable[[], datetime]
    _repositorio
    \_\_init\_\_(adaptador: AdaptadorBlast, repositorio: RepositorioHistorial, reloj: Callable[[], datetime]) None
    ejecutar_busqueda(configuracion: dict) list[dict]
  }
  class ErrorBlast {
  }
  class Hit {
    descripcion : str
    evalue : float
    id_hit : str
    identidades : int
    longitud_alineamiento : int
    query_desde : int
    query_hasta : int
    score : float
  }
  class RepositorioHistorial {
    guardar(busqueda: 'Busqueda')* None
  }
  class RepositorioHistorialEnMemoria {
    _candado : lock
    _guardadas : list[Busqueda]
    busquedas_guardadas : tuple['Busqueda', ...]
    \_\_init\_\_() None
    guardar(busqueda: 'Busqueda') None
  }
  class RepositorioHistorialSqlite {
    _conexion
    \_\_init\_\_(conexion: ConexionBD) None
    guardar(busqueda: 'Busqueda') None
  }
  class ResultadoComando {
    codigo : int
    errores : str
    salida : str
    \_\_init\_\_(self, codigo: int, salida: str, errores: str) None
  }
  class SolicitudEjecucion {
    base_datos : str
    model_config : ConfigDict
    modo : Literal['local', 'remoto']
    parametros : dict[str, int | float | str]
    secuencia : str
    variante : Literal['blastn', 'blastp', 'blastx', 'tblastn', 'tblastx']
  }
  RepositorioHistorialEnMemoria --|> RepositorioHistorial
  RepositorioHistorialSqlite --|> RepositorioHistorial
  AdaptadorBlastCli --|> AdaptadorBlast
  Busqueda --> Alineamiento : _alineamientos
  RepositorioHistorialEnMemoria --> Busqueda : _guardadas
  ConexionBD --o RepositorioHistorialSqlite : _conexion
  RepositorioHistorial --o ControladorEjecucion : _repositorio
  AdaptadorBlast --o ControladorEjecucion : _adaptador
```
