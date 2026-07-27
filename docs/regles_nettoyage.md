# Règles de nettoyage — Online Retail II

## 1. Customer ID manquant
- Règle : conserver, remplacer par "Anonymous"
- Justification : permet de garder le CA total réel ; exclu uniquement de la segmentation client

## 2. Quantity négative (annulations/retours)
- Règle : isoler dans un flux séparé (df_annulations), ne pas supprimer
- Justification : utile pour la détection d'anomalies

## 3. Price <= 0
- Règle : isoler dans df_anomalies_prix
- Justification : ajustements internes, faussent le calcul du CA

## 4. Codes produits non commerciaux (POST, DOT, M, BANK CHARGES...)
- Règle : exclure du flux de ventes produits
- Justification : ne représentent pas de vraies transactions produit

## 5. Doublons exacts
- Règle : suppression
- Justification : évite le double comptage