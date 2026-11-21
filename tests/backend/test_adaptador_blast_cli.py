"""AdaptadorBlastCli: invocación de BLAST+ y lectura de su salida (caja blanca por caminos).

BLAST+ se reemplaza por un ejecutor doble, así que estas pruebas no necesitan BLAST+ instalado.
"""

import subprocess
from pathlib import Path

import pytest

from backend.adaptador_blast.adaptador_blast import ErrorBlast
from backend.adaptador_blast.adaptador_blast_cli import AdaptadorBlastCli, ResultadoComando
from conftest import QUERY_420, armar_salida_xml


class EjecutorDoble:
    """Hace de BLAST+: registra el comando y la entrada, y devuelve un resultado fijo o lanza."""

    def __init__(self, resultado: ResultadoComando | None = None, excepcion: Exception | None = None):
        """Configura el resultado que devolverá o la excepción que lanzará."""
        self.resultado = resultado or ResultadoComando(0, armar_salida_xml({"id": "h1"}), "")
        self.excepcion = excepcion
        self.comando: list[str] | None = None
        self.entrada: str | None = None

    def __call__(self, comando, entrada, directorio, limite_segundos):
        """Registra el comando y la entrada, y responde lo configurado."""
        self.comando, self.entrada = comando, entrada
        if self.excepcion is not None:
            raise self.excepcion
        return self.resultado


def ejecutar(adaptador, variante="blastp", base="base", remota=False, parametros=None):
    """Ejecuta el adaptador con la query de prueba y los valores indicados."""
    return adaptador.ejecutar(variante, QUERY_420, base, remota, parametros or {})


# --- AdaptadorBlastCli.ejecutar (complejidad 5) ---------------------------------------

def test_devuelve_los_hits_leidos_y_pasa_la_query_por_la_entrada_estandar():
    """CP-21 · Caja blanca, camino principal."""
    ejecutor = EjecutorDoble(ResultadoComando(0, armar_salida_xml(
        {"id": "h1", "def": "Primera", "bits": 887.1, "evalue": 0, "ident": 419, "largo": 420,
         "desde": 1, "hasta": 420},
    ), ""))

    hits = ejecutar(AdaptadorBlastCli(ejecutor))

    assert hits == [{
        "id_hit": "h1", "descripcion": "Primera", "score": 887.1, "evalue": 0.0,
        "identidades": 419, "longitud_alineamiento": 420, "query_desde": 1, "query_hasta": 420,
    }]
    assert ejecutor.entrada == QUERY_420


def test_si_blast_no_esta_instalado_lanza_error_blast():
    """CP-22 · Caja blanca, rama "no se encontró el programa"."""
    adaptador = AdaptadorBlastCli(EjecutorDoble(excepcion=FileNotFoundError()))

    with pytest.raises(ErrorBlast, match="No se encontró el programa 'blastp'"):
        ejecutar(adaptador)


def test_si_blast_supera_el_tiempo_limite_lanza_error_blast():
    """CP-23 · Caja blanca, rama "se superó el tiempo límite"."""
    excepcion = subprocess.TimeoutExpired(cmd="blastp", timeout=5)
    adaptador = AdaptadorBlastCli(EjecutorDoble(excepcion=excepcion), limite_segundos=5)

    with pytest.raises(ErrorBlast, match="no terminó dentro del límite de 5 segundos"):
        ejecutar(adaptador)


def test_si_blast_falla_el_error_lleva_su_mensaje_literal():
    """CP-24 · Caja blanca, rama "código distinto de 0 con mensaje" · R4: mensaje literal de
    BLAST+.
    """
    mensaje = "BLAST Database error: No alias or index file found for protein database [x]"
    adaptador = AdaptadorBlastCli(EjecutorDoble(ResultadoComando(2, "", f"{mensaje}\n")))

    with pytest.raises(ErrorBlast) as error:
        ejecutar(adaptador)
    assert str(error.value) == mensaje


def test_si_blast_falla_sin_mensaje_el_error_informa_el_codigo():
    """CP-25 · Caja blanca, rama "código distinto de 0 sin mensaje"."""
    adaptador = AdaptadorBlastCli(EjecutorDoble(ResultadoComando(3, "", "   ")))

    with pytest.raises(ErrorBlast, match="terminó con código 3"):
        ejecutar(adaptador)


# --- AdaptadorBlastCli._armar_comando (complejidad 5) -----------------------------------

def test_arma_el_comando_basico_de_una_busqueda_local():
    """CP-26 · Caja blanca, búsqueda local sin parámetros y sin carpeta de BLAST+."""
    ejecutor = EjecutorDoble()
    ejecutar(AdaptadorBlastCli(ejecutor), base="datos/blastdb/proteinas_demo")

    assert ejecutor.comando == ["blastp", "-db", "datos/blastdb/proteinas_demo", "-outfmt", "5"]


def test_una_busqueda_remota_agrega_la_opcion_remote():
    """CP-27 · Caja blanca, rama "remota"."""
    ejecutor = EjecutorDoble()
    ejecutar(AdaptadorBlastCli(ejecutor), base="swissprot", remota=True)

    assert ejecutor.comando == ["blastp", "-db", "swissprot", "-outfmt", "5", "-remote"]


def test_traduce_los_parametros_conocidos_e_ignora_los_demas():
    """CP-28 · Caja blanca, ciclo de parámetros: los conocidos se traducen y los demás se ignoran.

    """
    ejecutor = EjecutorDoble()
    parametros = {"matrix": "BLOSUM62", "evalue": 0.001, "desconocido": "x", "word_size": 3}
    ejecutar(AdaptadorBlastCli(ejecutor), parametros=parametros)

    assert ejecutor.comando[5:] == ["-evalue", "0.001", "-word_size", "3", "-matrix", "BLOSUM62"]


def test_usa_la_carpeta_de_blast_configurada():
    """CP-29 · Caja blanca, rama "carpeta de BLAST+ configurada"."""
    ejecutor = EjecutorDoble()
    ejecutar(AdaptadorBlastCli(ejecutor, directorio_blast=Path("/opt/blast/bin")), variante="blastn")

    assert ejecutor.comando[0] == str(Path("/opt/blast/bin") / "blastn")


# --- AdaptadorBlastCli.leer_salida (complejidad 5) y _leer_hit (complejidad 3) ----------

def test_una_salida_que_no_es_xml_lanza_error_blast():
    """CP-30 · Caja blanca, rama "XML inválido"."""
    with pytest.raises(ErrorBlast, match="no es un XML válido"):
        AdaptadorBlastCli().leer_salida("esto no es XML")


def test_una_salida_sin_hits_devuelve_una_lista_vacia_sin_advertencias(caplog):
    """CP-31 · Caja blanca, ciclo de hits sin iteraciones (BLAST+ no encontró nada)."""
    assert AdaptadorBlastCli().leer_salida(armar_salida_xml()) == []
    assert caplog.records == []


def test_un_hit_sin_alineamientos_lanza_error_blast():
    """CP-32 · Caja blanca, _leer_hit rama "hit sin Hsp"."""
    xml = armar_salida_xml({"id": "h1"})
    inicio, fin = xml.index("<Hit_hsps>"), xml.index("</Hit_hsps>") + len("</Hit_hsps>")

    with pytest.raises(ErrorBlast, match="sin alineamientos"):
        AdaptadorBlastCli().leer_salida(xml[:inicio] + xml[fin:])


def test_con_identificador_ordinal_se_toma_el_id_de_la_definicion():
    """CP-33 · Caja blanca, _leer_hit rama "base creada sin -parse_seqids"."""
    xml = armar_salida_xml({"id": "gnl|BL_ORD_ID|7", "def": "demo_var08 Variante sintetica"})

    (hit,) = AdaptadorBlastCli().leer_salida(xml)

    assert (hit["id_hit"], hit["descripcion"]) == ("demo_var08", "Variante sintetica")
