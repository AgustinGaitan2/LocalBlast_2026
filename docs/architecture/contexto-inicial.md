El diagrama de nivel cero o diagrama de contexto inicial corresponde a: 

```mermaid
graph TD
    A["Usuario<br/>(Envía secuencia)"]
    B(("LocalBlast_2026<br/>"))
    C["Motor BLAST<br/>(NCBI / local)"]

    A <-->|Consulta y resultados| B
    B <-->|Alineamiento| C
