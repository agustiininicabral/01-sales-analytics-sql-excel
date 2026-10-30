"""Execute the PostgreSQL schema, load the sample CSVs, and smoke-test analytics SQL."""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd
import sqlalchemy as sa
from sqlalchemy import text

ROOT = Path(__file__).resolve().parents[1]


def statements(path: Path) -> list[str]:
    """Split the repository's simple, single-statement-per-semicolon SQL files."""
    output = []
    for chunk in path.read_text(encoding="utf-8").split(";"):
        lines = [line for line in chunk.splitlines() if not line.lstrip().startswith("--")]
        statement = "\n".join(lines).strip()
        if statement:
            output.append(statement)
    return output


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--db", required=True, help="SQLAlchemy PostgreSQL connection URL")
    parser.add_argument("--data", default=str(ROOT / "data"))
    args = parser.parse_args()

    engine = sa.create_engine(args.db)
    data_dir = Path(args.data)

    with engine.begin() as connection:
        for statement in statements(ROOT / "sql" / "schema.sql"):
            connection.execute(text(statement))

    tables = (
        ("customers", "dim_customer", "signup_date"),
        ("sellers", "dim_seller", None),
        ("products", "dim_product", None),
        ("sales", "fact_sale", "sale_date"),
    )
    for source, target, date_column in tables:
        options = {"parse_dates": [date_column]} if date_column else {}
        frame = pd.read_csv(data_dir / f"{source}.csv", **options)
        frame.to_sql(target, engine, if_exists="append", index=False)

    queries = statements(ROOT / "sql" / "queries.sql")
    if len(queries) != 5:
        raise AssertionError(f"Expected 5 analytical queries, found {len(queries)}")

    with engine.connect() as connection:
        results = [connection.execute(text(query)).fetchall() for query in queries]
        database_total = connection.execute(
            text("SELECT SUM(net_amount) FROM fact_sale")
        ).scalar_one()

    monthly, top_products, averages, repeat_customers, category_margin = results
    if not monthly or abs(sum(float(row[1]) for row in monthly) - float(database_total)) > 0.01:
        raise AssertionError("Monthly sales do not reconcile with fact_sale")
    if not 1 <= len(top_products) <= 10:
        raise AssertionError("Top-products query returned an unexpected number of rows")
    if not averages or averages[0][0] is None or float(averages[0][0]) <= 0:
        raise AssertionError("Average ticket query returned an invalid result")
    if not repeat_customers:
        raise AssertionError("Recurring-customer query returned no rows")
    if not category_margin or any(row[1] is None for row in category_margin):
        raise AssertionError("Category-margin query returned an invalid result")

    print(
        "POSTGRESQL PASS: "
        f"{len(monthly)} monthly periods, {len(top_products)} top products, "
        f"{len(repeat_customers)} recurring customers, "
        f"{len(category_margin)} categories; net sales reconciled."
    )
    engine.dispose()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
