"""Validate the sales analytics CSV files."""

import argparse
import csv
import json
from datetime import date
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TABLES = {
    "customers": {"customer_id", "customer_name", "city", "segment", "signup_date"},
    "products": {"product_id", "sku", "product_name", "category", "unit_cost", "unit_price"},
    "sellers": {"seller_id", "seller_name", "team"},
    "sales": {"sale_id", "sale_date", "customer_id", "seller_id", "product_id", "quantity", "unit_price", "discount_rate", "net_amount"},
}


def validate_directory(data_dir):
    tables = {}
    errors = []
    for name, required in TABLES.items():
        path = Path(data_dir) / f"{name}.csv"
        if not path.is_file():
            tables[name] = []
            errors.append(f"Missing file: {name}.csv")
            continue
        with path.open(newline="", encoding="utf-8-sig") as stream:
            reader = csv.DictReader(stream)
            missing = required - set(reader.fieldnames or [])
            if missing:
                tables[name] = []
                errors.append(f"{name}.csv missing columns: {', '.join(sorted(missing))}")
            else:
                tables[name] = list(reader)
        if not tables[name]:
            errors.append(f"{name}.csv has no data rows")

    for table, key in (("customers", "customer_id"), ("products", "product_id"), ("products", "sku"), ("sellers", "seller_id"), ("sales", "sale_id")):
        values = [row.get(key, "").strip() for row in tables[table]]
        if any(not value for value in values) or len(values) != len(set(values)):
            errors.append(f"{table}.{key} contains blank or duplicate values")

    customer_ids = {row.get("customer_id", "") for row in tables["customers"]}
    product_ids = {row.get("product_id", "") for row in tables["products"]}
    seller_ids = {row.get("seller_id", "") for row in tables["sellers"]}
    for row in tables["customers"]:
        try:
            date.fromisoformat(row["signup_date"])
        except (KeyError, ValueError):
            errors.append(f"customer {row.get('customer_id', '?')}: invalid signup date")
    for row in tables["products"]:
        try:
            cost, price = float(row["unit_cost"]), float(row["unit_price"])
            if cost < 0 or price <= 0 or cost > price:
                errors.append(f"product {row.get('product_id', '?')}: invalid cost/price")
        except (KeyError, ValueError):
            errors.append(f"product {row.get('product_id', '?')}: non-numeric cost/price")
    for row in tables["sales"]:
        sale_id = row.get("sale_id", "?")
        if row.get("customer_id", "") not in customer_ids:
            errors.append(f"sale {sale_id}: unknown customer")
        if row.get("product_id", "") not in product_ids:
            errors.append(f"sale {sale_id}: unknown product")
        if row.get("seller_id", "") not in seller_ids:
            errors.append(f"sale {sale_id}: unknown seller")
        try:
            date.fromisoformat(row["sale_date"])
            quantity = int(row["quantity"])
            price = Decimal(row["unit_price"])
            discount = Decimal(row["discount_rate"])
            net = Decimal(row["net_amount"])
            if quantity <= 0 or price <= 0 or net < 0 or not 0 <= discount <= 1:
                errors.append(f"sale {sale_id}: invalid numeric values")
            expected = (quantity * price * (Decimal("1") - discount)).quantize(
                Decimal("0.01"), rounding=ROUND_HALF_UP
            )
            if abs(net - expected) > Decimal("0.01"):
                errors.append(f"sale {sale_id}: net amount does not reconcile")
        except (KeyError, ValueError):
            errors.append(f"sale {sale_id}: invalid date or numeric value")

    return {"status": "PASS" if not errors else "FAIL",
            "row_counts": {name: len(rows) for name, rows in tables.items()},
            "failure_count": len(errors), "failures": errors}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-dir", default=str(ROOT / "data"))
    parser.add_argument("--out", default=str(ROOT / "reports" / "data_quality_report.json"))
    args = parser.parse_args()
    report = validate_directory(args.data_dir)
    output = Path(args.out)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"{report['status']}: {sum(report['row_counts'].values())} rows; {report['failure_count']} failures")
    return 0 if not report["failures"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
