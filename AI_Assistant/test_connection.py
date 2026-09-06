from connection import connect_warehouse


print("Connexion à Microsoft Fabric...")

try:
    conn = connect_warehouse()

    print("Connexion réussie !")

    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*) AS nb_lignes
        FROM fact_sales
    """)

    row = cursor.fetchone()

    print(f"Nombre de lignes fact_sales : {row[0]}")

    cursor.close()
    conn.close()

    print("Connexion fermée.")

except Exception as e:
    print("Erreur :")
    print(e)