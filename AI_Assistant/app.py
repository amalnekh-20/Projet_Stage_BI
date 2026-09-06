import time

import streamlit as st
from assistant import repondre_question


# ============================================================
# CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="AI Assistant BI",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# STYLE CSS
# ============================================================

st.markdown("""
<style>

    /* Arrière-plan général */
    .stApp {
        background-color: #f5f7fb;
    }

    /* Conteneur principal */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1200px;
    }

    /* Header */
    .main-header {
        background: linear-gradient(135deg, #1f4e79, #2563a6);
        padding: 30px 35px;
        border-radius: 16px;
        color: white;
        margin-bottom: 25px;
        box-shadow: 0 8px 25px rgba(31, 78, 121, 0.15);
    }

    .main-header h1 {
        margin: 0;
        font-size: 34px;
        font-weight: 700;
    }

    .main-header p {
        margin-top: 8px;
        margin-bottom: 0;
        font-size: 16px;
        opacity: 0.9;
    }

    /* Cartes KPI */
    .info-card {
        background-color: white;
        padding: 20px;
        border-radius: 14px;
        border: 1px solid #e5e7eb;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.04);
        height: 100%;
    }

    .info-card-title {
        font-size: 14px;
        color: #6b7280;
        margin-bottom: 8px;
    }

    .info-card-value {
        font-size: 18px;
        font-weight: 600;
        color: #1f2937;
    }

    /* Zone question */
    .question-title {
        font-size: 20px;
        font-weight: 600;
        color: #1f2937;
        margin-top: 20px;
        margin-bottom: 10px;
    }

    /* Titre de la zone réponse (le cadre lui-même vient de st.container(border=True)) */
    .response-title {
        font-size: 18px;
        font-weight: 600;
        color: #1f4e79;
        margin-bottom: 15px;
    }

    /* Bouton */
    .stButton > button {
        width: 100%;
        border-radius: 10px;
        height: 45px;
        font-weight: 600;
        border: none;
        background-color: #1f4e79;
        color: white;
    }

    .stButton > button:hover {
        background-color: #173a5c;
        color: white;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid #e5e7eb;
    }

    /* Footer */
    .footer {
        text-align: center;
        color: #9ca3af;
        font-size: 13px;
        margin-top: 50px;
        padding-top: 20px;
        border-top: 1px solid #e5e7eb;
    }

</style>
""", unsafe_allow_html=True)


# ============================================================
# ÉTAT DE SESSION
# ============================================================
# Le champ de question est piloté par session_state pour que les
# boutons "exemples" puissent le pré-remplir de façon fiable.
if "question_input" not in st.session_state:
    st.session_state.question_input = ""


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown("## 📊 AI Assistant BI")

    st.markdown("---")

    st.markdown("### Domaines disponibles")

    st.markdown("""
    **💰 Chiffre d'affaires**
    Analyse du CA total.

    **📦 Produits**
    Identification des produits les plus performants.

    **🌍 Pays**
    Analyse des ventes par pays.

    **📈 Évolution mensuelle**
    Analyse de la tendance du chiffre d'affaires.

    **↩️ Retours**
    Analyse du taux de retour.
    """)

    st.markdown("---")

    st.markdown("### Comment utiliser l'assistant ?")

    st.markdown("""
    1. Saisissez votre question.
    2. Cliquez sur **Analyser**.
    3. L'assistant récupère les KPI nécessaires.
    4. Gemini génère une réponse à partir des données.
    """)

    st.markdown("---")

    st.caption("Assistant BI — Projet de stage")


# ============================================================
# HEADER PRINCIPAL
# ============================================================

st.markdown("""
<div class="main-header">
    <h1>📊 AI Assistant BI</h1>
    <p>Assistant intelligent d'analyse des données commerciales</p>
</div>
""", unsafe_allow_html=True)


# ============================================================
# CARTES D'INFORMATION
# ============================================================

card_col1, card_col2, card_col3 = st.columns(3)

with card_col1:
    st.markdown("""
    <div class="info-card">
        <div class="info-card-title">Source des données</div>
        <div class="info-card-value">Microsoft Fabric</div>
    </div>
    """, unsafe_allow_html=True)

with card_col2:
    st.markdown("""
    <div class="info-card">
        <div class="info-card-title">Intelligence artificielle</div>
        <div class="info-card-value">Google Gemini</div>
    </div>
    """, unsafe_allow_html=True)

with card_col3:
    st.markdown("""
    <div class="info-card">
        <div class="info-card-title">Type d'analyse</div>
        <div class="info-card-value">Business Intelligence</div>
    </div>
    """, unsafe_allow_html=True)


# ============================================================
# EXEMPLES DE QUESTIONS
# ============================================================
# Placés AVANT le text_input pour pouvoir modifier
# st.session_state.question_input avant que le widget ne soit instancié
# sur ce rerun (obligatoire avec Streamlit : on ne peut pas modifier la
# valeur d'un widget après sa création dans le même run).

st.markdown("**Exemples de questions :**")

ex_col1, ex_col2, ex_col3, ex_col4 = st.columns(4)

exemples = {
    "💰 CA total": "Quel est le chiffre d'affaires total ?",
    "📦 Top produits": "Quel est le produit qui génère le plus de chiffre d'affaires ?",
    "🌍 Ventes par pays": "Quel pays génère le plus de ventes ?",
    "↩️ Taux de retour": "Quel est le taux de retour ?",
}

for col, (label, texte) in zip((ex_col1, ex_col2, ex_col3, ex_col4), exemples.items()):
    with col:
        if st.button(label, use_container_width=True, key=f"exemple_{label}"):
            st.session_state.question_input = texte
            st.rerun()


# ============================================================
# ZONE DE QUESTION
# ============================================================

st.markdown(
    '<div class="question-title">Posez votre question</div>',
    unsafe_allow_html=True
)

question = st.text_input(
    "Votre question",
    placeholder="Exemple : Quel est le chiffre d'affaires total ?",
    label_visibility="collapsed",
    key="question_input",
)


# ============================================================
# BOUTON ANALYSER
# ============================================================

if st.button("Analyser la question", type="primary"):

    if not question.strip():
        st.warning("Veuillez saisir une question.")
    else:
        with st.spinner("Analyse des données en cours..."):
            try:
                debut = time.perf_counter()
                reponse = repondre_question(question)
                duree = time.perf_counter() - debut

                with st.container(border=True):
                    st.markdown(
                        '<div class="response-title">🤖 Réponse de l\'assistant</div>',
                        unsafe_allow_html=True,
                    )
                    st.markdown(reponse)
                    st.caption(f"Temps de réponse Gemini/Fabric : {duree:.2f} s")

            except Exception as e:

              erreur = str(e)

              if "503" in erreur or "UNAVAILABLE" in erreur:
                  st.warning(
                      "Le service Gemini est temporairement indisponible "
                      "en raison d'une forte demande. "
                      "Veuillez réessayer dans quelques instants."
                  )

              else:
                  st.error(
                      f"Une erreur est survenue lors de l'analyse : {e}"
                  )


# ============================================================
# FOOTER
# ============================================================

st.markdown("""
<div class="footer">
    AI Assistant BI · Microsoft Fabric · Google Gemini
</div>
""", unsafe_allow_html=True)