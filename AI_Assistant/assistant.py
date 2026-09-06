import json
import os

from dotenv import load_dotenv
from google import genai

from connection import get_kpi_context
from kpi_queries import detecter_kpi_pertinents


# Charger les variables d'environnement
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError(
        "GEMINI_API_KEY n'est pas définie dans le fichier .env"
    )


# Client Gemini
client = genai.Client(api_key=api_key)


def repondre_question(question):
    """
    Analyse la question, récupère les KPI pertinents
    depuis Microsoft Fabric et demande à Gemini
    de générer une réponse.
    """

    # 1. Detecter les KPI necessaires
    kpi_pertinents = detecter_kpi_pertinents(question)

    if not kpi_pertinents:
      return (
          "Je peux répondre uniquement aux questions liées "
          "aux données de ventes disponibles : chiffre d'affaires, "
          "produits, pays, évolution mensuelle et taux de retour."
      )

    # 2. Recuperer les donnees depuis Fabric
    contexte = get_kpi_context(kpi_pertinents)

    # 3. Preparer le contexte pour Gemini
    contexte_json = json.dumps(
        contexte,
        ensure_ascii=False,
        indent=2
    )

    # 4. Prompt systeme / instructions
    prompt = f"""
Tu es un assistant d'aide à la décision pour une entreprise
de commerce en ligne.

Tu dois répondre uniquement à partir des données fournies
dans le contexte ci-dessous.

Règles :
- N'invente aucune donnée.
- Si l'information demandée n'est pas disponible,
  indique clairement qu'elle n'est pas disponible.
- Réponds en français.
- Sois précis et concis.
- Lorsque c'est pertinent, présente les montants avec
  deux chiffres après la virgule.
- Ne donne pas d'informations qui ne peuvent pas être
  déduites des données fournies.

CONTEXTE DES DONNÉES :
{contexte_json}

QUESTION DE L'UTILISATEUR :
{question}
"""

    # 5. Appel a Gemini
    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=prompt
    )

    return response.text
