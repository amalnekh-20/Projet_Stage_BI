import sys
import pandas as pd
import pytest

# Ajout du chemin vers le dossier scripts
sys.path.append("C:/Users/hp/projet-stage-bi/scripts")
from clean_data import clean_data


@pytest.fixture
def sample_data():
    """Jeu de données de test couvrant tous les cas métier."""
    return pd.DataFrame({
        "Invoice": ["536365", "536365", "C536379", "536366", "536367"],
        "StockCode": ["85123A", "85123A", "D", "84029G", "22622"],
        "Description": ["WHITE HANGING HEART", "WHITE HANGING HEART", "Discount", "HAND WARMER", "BOX OF 6 TEAS"],
        "Quantity": [6, 6, -1, 2, 1],  # La 2e ligne est un doublon exact
        "InvoiceDate": pd.to_datetime(["2010-12-01 08:26:00"] * 5),
        "Price": [2.55, 2.55, 10.00, 0.00, 4.25],
        "Customer ID": [17850.0, 17850.0, 17850.0, 17850.0, 13047.0],
        "Country": ["United Kingdom"] * 5
    })


def test_suppression_doublons(sample_data):
    """Vérifie que les doublons exacts sont bien supprimés."""
    resultats = clean_data(sample_data)
    
    # La ligne 1 était un doublon parfait de la ligne 0
    total_lignes = sum(len(df) for df in resultats.values())
    assert total_lignes == 4


def test_calcul_total_price(sample_data):
    """Vérifie le calcul de TotalPrice (Quantity * Price)."""
    resultats = clean_data(sample_data)
    df_ventes = resultats["ventes"]
    
    # Pour la ligne 4 (Quantity: 1, Price: 4.25)
    ligne_tea = df_ventes[df_ventes["StockCode"] == "22622"].iloc[0]
    assert ligne_tea["TotalPrice"] == 4.25


def test_separation_annulations(sample_data):
    """Vérifie l'isolement des annulations (Quantity < 0 ou Invoice commençant par C)."""
    resultats = clean_data(sample_data)
    df_annulations = resultats["annulations"]
    
    assert len(df_annulations) == 1
    assert df_annulations.iloc[0]["Invoice"] == "C536379"


def test_separation_anomalies_prix(sample_data):
    """Vérifie l'isolement des articles vendus à prix nul (Price == 0)."""
    resultats = clean_data(sample_data)
    df_anomalies = resultats["anomalies_prix"]
    
    assert len(df_anomalies) == 1
    assert df_anomalies.iloc[0]["Price"] == 0.00