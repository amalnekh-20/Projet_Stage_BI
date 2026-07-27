## Résultat du nettoyage (Jour 5)

### Avant nettoyage
- Nombre total de lignes : 1 067 371
- Nombre de colonnes : 8

### Traitements appliqués
- Doublons exacts supprimés : 34 335 lignes

### Répartition après nettoyage (4 flux distincts)

| Flux | Nombre de lignes | Description |
|---|---|---|
| Ventes valides | 1 003 495 | Transactions propres, prêtes pour l'ETL et l'analyse |
| Annulations isolées | 21 475 | Quantités négatives (retours/annulations) |
| Anomalies de prix isolées | 2 602 | Prix ≤ 0 (ajustements internes) |
| Codes non commerciaux isolés | 5 464 | POST, DOT, M, BANK CHARGES, etc. |
| **Total** | **1 033 036** | |

### Vérification de cohérence

1 067 371 (avant nettoyage)
-  34 335 (doublons supprimés)
= 1 033 036 (total des 4 flux) - conforme

Aucune ligne n'a été perdue au-delà des doublons supprimés.

### Fichiers générés
- data/clean/ventes.parquet (1 003 495 lignes)
- data/clean/annulations.parquet (21 475 lignes)
- data/clean/anomalies_prix.parquet (2 602 lignes)
- data/clean/non_commercial.parquet (5 464 lignes)