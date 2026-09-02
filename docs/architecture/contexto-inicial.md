El diagrama de nivel cero o diagrama de contexto inicial de este proyecto corresponde a: 

```mermaid
graph TD
    A["Usuario<br/>(Envía secuencia)"]
    B(("LocalBlast_2026<br/>"))
    C["Motor BLAST<br/>(NCBI / local)"]

    A <-->|Consulta y resultados| B
    B <-->|Alineamiento| C
```

Donde un usuario es un actor que envia una secuencia a la aplicacion principal y seguido
de una validacion de dicha secuencia se lleva a cabo una consulta o query a una API. Es asi que a partir
de un alineamiento local con otras secuencias en la BD del NCBI, el usuario
obtiene el resultado de su consulta.
