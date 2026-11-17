"""RepositorioHistorialSql (componente Acceso a datos, capa de datos).

Guarda el historial D2 en una base relacional con SQLAlchemy. La misma clase
funciona con SQLite (desarrollo y defensa) o con PostgreSQL (producción, según la
arquitectura) cambiando solo ``url_conexion`` (decisión D9).

La búsqueda y todos sus alineamientos crudos se escriben en una sola transacción:
o queda todo, o no queda nada (CA-03 y garantía mínima de CU004).
"""

import json

from sqlalchemy import (
    Boolean, Column, DateTime, Float, ForeignKey, Integer, MetaData, String, Table, Text,
    create_engine,
)

from aplicacion.repositorio_historial import RepositorioHistorial
from dominio.busqueda import Busqueda

metadata = MetaData()

tabla_busquedas = Table(
    "busquedas",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("fecha", DateTime, nullable=False),
    Column("programa", String(20), nullable=False),
    Column("base_datos", String(255), nullable=False),
    Column("remota", Boolean, nullable=False),
    Column("secuencia", Text, nullable=False),
    Column("parametros", Text, nullable=False),
)

tabla_alineamientos = Table(
    "alineamientos",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("busqueda_id", Integer, ForeignKey("busquedas.id"), nullable=False),
    Column("hit_id", String(255), nullable=False),
    Column("descripcion", Text, nullable=False),
    Column("score", Float, nullable=False),
    Column("evalue", Float, nullable=False),
    Column("identidades", Integer, nullable=False),
    Column("longitud_alineamiento", Integer, nullable=False),
    Column("query_desde", Integer, nullable=False),
    Column("query_hasta", Integer, nullable=False),
)


class RepositorioHistorialSql(RepositorioHistorial):
    def __init__(self, url_conexion: str) -> None:
        self.url_conexion = url_conexion
        self._motor = create_engine(url_conexion)
        metadata.create_all(self._motor)

    def guardar(self, busqueda: Busqueda) -> None:
        with self._motor.begin() as conexion:  # una sola transacción
            resultado = conexion.execute(
                tabla_busquedas.insert().values(
                    fecha=busqueda.fecha,
                    programa=busqueda.programa,
                    base_datos=busqueda.base_datos,
                    remota=busqueda.remota,
                    secuencia=busqueda.secuencia,
                    parametros=json.dumps(busqueda.parametros),
                )
            )
            busqueda_id = resultado.inserted_primary_key[0]
            filas = [
                {
                    "busqueda_id": busqueda_id,
                    "hit_id": a.hit_id,
                    "descripcion": a.descripcion,
                    "score": a.score,
                    "evalue": a.evalue,
                    "identidades": a.identidades,
                    "longitud_alineamiento": a.longitud_alineamiento,
                    "query_desde": a.query_desde,
                    "query_hasta": a.query_hasta,
                }
                for a in busqueda.alineamientos
            ]
            if filas:
                conexion.execute(tabla_alineamientos.insert(), filas)

    def cerrar(self) -> None:
        """Libera las conexiones abiertas (al apagar el programa o al terminar una prueba)."""
        self._motor.dispose()
