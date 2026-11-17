"""Datos de demostración para AdaptadorBlastSimulado.

Permiten mostrar la HU funcionando en una máquina sin BLAST+: la secuencia de
demostración contra ``base_demo`` devuelve estos hits; otra secuencia no tiene
hits (tabla vacía), y cualquier otra base termina con el mismo error que daría
BLAST+ (camino de rechazo).
"""

SECUENCIA_DEMO = (
    ">query_demo fragmento del gen 16S rRNA\n"
    "AGAGTTTGATCCTGGCTCAGATTGAACGCTGGCGGCAGGCCTAACACATGCAAGTCGAACGGTAACAGGAAG\n"
    "AAGCTTGCTTCTTTGCTGACGAGTGGCGGACGGGTGAGTAATGTCTGGGAAACTGCCTGATGGAGGGGGATA"
)

BASES_DEMO = {"base_demo"}

HITS_DEMO = [
    {"hit_id": "NR_024570.1", "descripcion": "Escherichia coli strain U 5/41 16S ribosomal RNA",
     "score": 268.5, "evalue": 2.1e-71, "identidades": 144, "longitud_alineamiento": 144,
     "query_desde": 1, "query_hasta": 144},
    {"hit_id": "NR_074902.1", "descripcion": "Shigella flexneri 2a str. 301 16S ribosomal RNA",
     "score": 263.0, "evalue": 9.8e-70, "identidades": 143, "longitud_alineamiento": 144,
     "query_desde": 1, "query_hasta": 144},
    {"hit_id": "NR_041980.1", "descripcion": "Salmonella enterica subsp. enterica 16S ribosomal RNA",
     "score": 230.1, "evalue": 7.4e-60, "identidades": 131, "longitud_alineamiento": 137,
     "query_desde": 8, "query_hasta": 144},
    {"hit_id": "NR_114042.1", "descripcion": "Klebsiella pneumoniae strain DSM 30104 16S ribosomal RNA",
     "score": 182.4, "evalue": 1.6e-45, "identidades": 112, "longitud_alineamiento": 123,
     "query_desde": 22, "query_hasta": 144},
]
