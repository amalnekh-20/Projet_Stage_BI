KPI_QUERIES = {

    "ca_total": """
        SELECT
            SUM(Revenue) AS CA_Total
        FROM fact_sales;
    """,

    "ca_par_mois": """
        SELECT
            d.Year,
            d.Month,
            SUM(f.Revenue) AS CA
        FROM fact_sales f
        INNER JOIN dim_date d
            ON f.DateKey = d.DateKey
        GROUP BY
            d.Year,
            d.Month
        ORDER BY
            d.Year,
            d.Month;
    """,

    "top_produits": """
        SELECT TOP 10
            p.StockCode,
            p.Description,
            SUM(f.Revenue) AS CA
        FROM fact_sales f
        INNER JOIN dim_product p
            ON f.ProductKey = p.ProductKey
        GROUP BY
            p.StockCode,
            p.Description
        ORDER BY
            CA DESC;
    """,

    "ca_par_pays": """
        SELECT
            c.Country,
            SUM(f.Revenue) AS CA
        FROM fact_sales f
        INNER JOIN dim_country c
            ON f.CountryKey = c.CountryKey
        GROUP BY
            c.Country
        ORDER BY
            CA DESC;
    """,

    "taux_retour": """
        SELECT
            CAST(
                SUM(
                    CASE
                        WHEN IsReturn = 1 THEN 1
                        ELSE 0
                    END
                ) AS FLOAT
            ) / COUNT(*) AS TauxRetour
        FROM fact_sales;
    """
}

def detecter_kpi_pertinents(question):
    question_lower = question.lower()

    kpi_a_charger = []

    if any(mot in question_lower for mot in [
        "produit", "article", "vendu", "performance"
    ]):
        kpi_a_charger.append("top_produits")

    if any(mot in question_lower for mot in [
        "pays", "géograph", "country", "destination"
    ]):
        kpi_a_charger.append("ca_par_pays")

    if any(mot in question_lower for mot in [
        "mois", "mensuel", "évolution", "tendance"
    ]):
        kpi_a_charger.append("ca_par_mois")

    if any(mot in question_lower for mot in [
        "retour", "retours", "annulation"
    ]):
        kpi_a_charger.append("taux_retour")

    if any(mot in question_lower for mot in [
        "chiffre d'affaires",
        "chiffre affaire",
        "ca",
        "revenu",
        "total",
        "ventes"
    ]):
        kpi_a_charger.append("ca_total")

    return list(dict.fromkeys(kpi_a_charger))