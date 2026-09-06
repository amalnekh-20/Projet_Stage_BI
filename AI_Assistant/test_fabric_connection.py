import struct

import pyodbc
from azure.identity import InteractiveBrowserCredential


SERVER = "7vijtkmceuye7elo7qdbw6rfrm-54sb6hausolenlayrdf3igefie.datawarehouse.fabric.microsoft.com"
DATABASE = "SalesLakehouse"

SQL_COPT_SS_ACCESS_TOKEN = 1256


print("Authentification Microsoft Entra...")

credential = InteractiveBrowserCredential()

token = credential.get_token(
    "https://database.windows.net/.default"
)

print("Token obtenu.")


token_bytes = token.token.encode("utf-16-le")

token_struct = struct.pack(
    f"<I{len(token_bytes)}s",
    len(token_bytes),
    token_bytes
)


connection_string = (
    "DRIVER={ODBC Driver 18 for SQL Server};"
    f"SERVER=tcp:{SERVER},1433;"
    f"DATABASE={DATABASE};"
    "Encrypt=yes;"
    "TrustServerCertificate=no;"
    "Connection Timeout=30;"
)


print("Connexion à Microsoft Fabric...")


try:
    conn = pyodbc.connect(
        connection_string,
        attrs_before={
            SQL_COPT_SS_ACCESS_TOKEN: token_struct
        }
    )

    print("Connexion réussie à Microsoft Fabric !")

    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*) AS nb_lignes
        FROM fact_sales
    """)

    row = cursor.fetchone()

    print("Nombre de lignes fact_sales :", row[0])

    cursor.close()
    conn.close()

    print("Connexion fermée.")

except pyodbc.Error as e:
    print("Erreur de connexion :")
    print(e)