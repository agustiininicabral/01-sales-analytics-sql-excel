from pathlib import Path
import csv

ROOT = Path(__file__).resolve().parents[1]


def load(name):
    with (ROOT / 'data' / f'{name}.csv').open(newline='', encoding='utf-8-sig') as handle:
        return list(csv.DictReader(handle))


def main():
    customers = load('customers')
    products = load('products')
    sellers = load('sellers')
    sales = load('sales')
    errors = []
    for table, key, rows in [('customers', 'customer_id', customers), ('products', 'product_id', products), ('sellers', 'seller_id', sellers), ('sales', 'sale_id', sales)]:
        values = [row[key] for row in rows]
        if len(values) != len(set(values)):
            errors.append(f'{table}: duplicate {key}')
    customer_ids = {row['customer_id'] for row in customers}
    product_ids = {row['product_id'] for row in products}
    seller_ids = {row['seller_id'] for row in sellers}
    for row in sales:
        if row['customer_id'] not in customer_ids or row['product_id'] not in product_ids or row['seller_id'] not in seller_ids:
            errors.append(f"sale {row['sale_id']}: unknown foreign key")
    print(f'rows: customers={len(customers)} products={len(products)} sellers={len(sellers)} sales={len(sales)}')
    for error in errors:
        print(error)
    return 1 if errors else 0


if __name__ == '__main__':
    raise SystemExit(main())
