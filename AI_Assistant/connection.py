import json
import struct

import pandas as pd
import pyodbc
from azure.identity import InteractiveBrowserCredential

from kpi_queries import KPI_QUERIES


SERVER = (
    "7vijtkmceuye7elo7qdbw6rfrm-54sb6hausolenlayrdf3igefie"
    ".datawarehouse.fabric.microsoft.com"
)

DATABASE = "SalesLakehouse"

SQL_COPT_SS_ACCESS_TOKEN = 1256


credential = InteractiveBrowserCredential()


def get_access_token():
    """Obtient un token Microsoft Entra pour Microsoft Fabric."""

    token = credential.get_token(
        "https://database.windows.net/.default"
    )

    return token.token


def connect_warehouse():
    """Établit une connexion authentifiée au SQL endpoint Fabric."""

    access_token = get_access_token()

    token_bytes = access_token.encode("utf-16-le")

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

    connection = pyodbc.connect(
        connection_string,
        attrs_before={
            SQL_COPT_SS_ACCESS_TOKEN: token_struct
        }
    )

    return connection


def get_kpi_context(kpi_names):
    """
    Exécute les requêtes SQL correspondant aux KPI demandés
    et retourne les résultats sous forme de dictionnaire.
    """

    conn = connect_warehouse()

    context = {}

    try:
        for name in kpi_names:

            if name not in KPI_QUERIES:
                raise ValueError(
                    f"KPI inconnu : {name}"
                )

            query = KPI_QUERIES[name]

            df = pd.read_sql(
                query,
                conn
            )

            context[name] = df.to_dict(
                orient="records"
            )

    finally:
        conn.close()

    return context