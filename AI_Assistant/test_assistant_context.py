from assistant import repondre_question


questions = [
    "Quel est le chiffre d'affaires total ?",
    "Quel est le produit qui génère le plus de chiffre d'affaires ?",
    "Quel pays génère le plus de ventes ?",
    "Comment évolue le chiffre d'affaires par mois ?",
    "Quel est le taux de retour ?",
]


for question in questions:

    print("=" * 70)
    print(f"QUESTION : {question}")
    print("-" * 70)

    try:
        reponse = repondre_question(question)
        print("RÉPONSE :")
        print(reponse)

    except Exception as e:
        print("ERREUR :")
        print(e)