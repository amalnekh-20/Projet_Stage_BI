import pandas as pd

from connection import connect_warehouse
from kpi_queries import KPI_QUERIES


def test_kpis():
    conn = connect_warehouse()

    try:
        for name, query in KPI_QUERIES.items():

            print("\n" + "=" * 60)
            print(f"KPI : {name}")
            print("=" * 60)

            df = pd.read_sql(query, conn)

            print(df.to_string(index=False))

    finally:
        conn.close()


if __name__ == "__main__":
    test_kpis()