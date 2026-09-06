import json

from assistant import get_kpi_context


kpi_names = [
    "ca_total",
    "top_produits",
    "ca_par_pays"
]


context = get_kpi_context(kpi_names)


print("\nContexte structuré :\n")

print(
    json.dumps(
        context,
        indent=4,
        ensure_ascii=False
    )
)