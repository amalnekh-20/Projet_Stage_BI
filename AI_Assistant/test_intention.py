from assistant import detecter_kpi_pertinents


QUESTIONS_TEST = [
    "Quel est le chiffre d'affaires total ?",
    "Quels sont les produits les plus performants ?",
    "Quel pays génère le plus de ventes ?",
    "Comment évolue le chiffre d'affaires par mois ?",
    "Quel est le taux de retour ?",
    "Quelle est la tendance des ventes ?",
    "Quelle est la météo à Paris ?"
]


for question in QUESTIONS_TEST:

    kpis = detecter_kpi_pertinents(question)

    print(f"\nQuestion : {question}")
    print(f"KPI détectés : {kpis}")