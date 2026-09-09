# Modelo de Dominio Conceptual — LocalBlast

Este modelo describe las **entidades esenciales del problema** y sus relaciones, en el nivel del TP1: sin atributos, sin tipos de dato, sin métodos ni visibilidad. El nivel de detalle interno de cada clase llega recién en el TP4 (diseño detallado).

Es un modelo del dominio del problema, no de la implementación: expresa "qué cosas existen y cómo se relacionan en el mundo del usuario", no cómo se van a codificar.

```mermaid
classDiagram
    class Usuario
    class Investigador
    class Administrador

    class Busqueda
    class SecuenciaQuery
    class ParametrosPreBusqueda
    class FiltroPostBusqueda
    class ModoEjecucion

    class BaseDeDatos
    class Alineamiento
    class Reporte
    class FormatoDescarga

    Usuario <|-- Investigador
    Usuario <|-- Administrador

    Investigador "1" --> "*" Busqueda : lanza
    Busqueda "1" --> "1" SecuenciaQuery : usa
    Busqueda "1" --> "1" ParametrosPreBusqueda : configurada con
    Busqueda "1" --> "1" ModoEjecucion : se ejecuta en
    Busqueda "1" --> "1" BaseDeDatos : consulta
    Busqueda "1" --> "*" Alineamiento : produce
    Busqueda "1" --> "*" FiltroPostBusqueda : refinada por
    Busqueda "1" --> "*" Reporte : origina
    Reporte "*" --> "1" FormatoDescarga : exportado en

    Administrador "1" --> "*" BaseDeDatos : administra
```

