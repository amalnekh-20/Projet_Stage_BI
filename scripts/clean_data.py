import pandas as pd

def load_raw_data(path="../data/raw/online_retail_full.parquet"):
    """Charge le dataset brut."""
    return pd.read_parquet(path)


def clean_data(df):
    """Applique les règles de nettoyage """
    
    df = df.copy()
    
    # Colonne utile pour la suite (ETL, dashboards)
    df["TotalPrice"] = df["Quantity"] * df["Price"]
    
    
    # Règle 1 : Customer ID manquant -> "Anonymous"
    # On convertit d'abord en texte proprement (ex: 17850.0 -> "17850"), puis on remplace les manquants
    df["Customer ID"] = df["Customer ID"].apply(
        lambda x: str(int(x)) if pd.notna(x) else "Anonymous"
    )
    
    # Règle 5 : suppression des doublons exacts
    nb_avant = len(df)
    df = df.drop_duplicates()
    print(f"Doublons supprimes : {nb_avant - len(df)}")
    
    # Règle 4 : isoler les codes non commerciaux
    codes_non_commerciaux = ["POST", "DOT", "M", "BANK CHARGES", "D", "C2", "CRUK"]
    mask_non_commercial = df["StockCode"].isin(codes_non_commerciaux)
    df_non_commercial = df[mask_non_commercial]
    df = df[~mask_non_commercial]
    
    # Règle 2 : isoler les annulations (Quantity negative)
    mask_annulation = df["Quantity"] < 0
    df_annulations = df[mask_annulation]
    df_ventes = df[~mask_annulation]
    
    # Règle 3 : isoler les prix <= 0
    mask_prix_suspect = df_ventes["Price"] <= 0
    df_anomalies_prix = df_ventes[mask_prix_suspect]
    df_ventes = df_ventes[~mask_prix_suspect]
    
    return {
        "ventes": df_ventes,
        "annulations": df_annulations,
        "anomalies_prix": df_anomalies_prix,
        "non_commercial": df_non_commercial,
    }


if __name__ == "__main__":
    df_raw = load_raw_data()
    resultats = clean_data(df_raw)
    
    for nom, sous_df in resultats.items():
        print(f"{nom} : {len(sous_df)} lignes")
        sous_df.to_parquet(f"../data/clean/{nom}.parquet")
    
    print("Nettoyage termine. Fichiers sauvegardes dans data/clean/")