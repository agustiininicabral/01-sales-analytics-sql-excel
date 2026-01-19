
import argparse
from pathlib import Path
import pandas as pd
import sqlalchemy as sa

def main():
    ap = argparse.ArgumentParser(description="Carga CSVs a PostgreSQL.")
    ap.add_argument("--db", required=True, help="SQLAlchemy URL. Ej: postgresql+psycopg2://user:pass@localhost:5432/dbname")
    ap.add_argument("--data", default="data", help="Carpeta con CSVs")
    args = ap.parse_args()

    engine = sa.create_engine(args.db)
    data_dir = Path(args.data)

    dim_customer = pd.read_csv(data_dir/"customers.csv", parse_dates=["signup_date"])
    dim_seller   = pd.read_csv(data_dir/"sellers.csv")
    dim_product  = pd.read_csv(data_dir/"products.csv")
    fact_sale    = pd.read_csv(data_dir/"sales.csv", parse_dates=["sale_date"])

    with engine.begin() as cxn:
        dim_customer.to_sql("dim_customer", cxn, if_exists="append", index=False)
        dim_seller.to_sql("dim_seller", cxn, if_exists="append", index=False)
        dim_product.to_sql("dim_product", cxn, if_exists="append", index=False)
        fact_sale.to_sql("fact_sale", cxn, if_exists="append", index=False)

    print("OK: Datos cargados.")

if __name__ == "__main__":
    main()