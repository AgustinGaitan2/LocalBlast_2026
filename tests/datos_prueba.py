"""Datos de prueba compartidos (constructores de hits y configuraciones)."""

from datetime import datetime

FECHA_FIJA = datetime(2026, 11, 16, 10, 30, 0)


def un_hit(hit_id: str = "NR_000001.1", **cambios) -> dict:
    """Hit como lo devuelve el adaptador: datos simples (decisión D5)."""
    hit = {
        "hit_id": hit_id,
        "descripcion": f"descripción de {hit_id}",
        "score": "200.5",
        "evalue": "1e-50",
        "identidades": "90",
        "longitud_alineamiento": "100",
        "query_desde": "1",
        "query_hasta": "100",
    }
    hit.update(cambios)
    return hit


def una_configuracion(secuencia: str = ">q1\n" + "A" * 100, **cambios) -> dict:
    configuracion = {
        "secuencia": secuencia,
        "programa": "blastn",
        "base_datos": "base_demo",
        "remota": False,
        "parametros": {"evalue": "0.001", "word_size": "11"},
    }
    configuracion.update(cambios)
    return configuracion
