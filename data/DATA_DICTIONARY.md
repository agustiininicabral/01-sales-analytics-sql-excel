# Data dictionary

All records are synthetic. No personal or company data is included.

## Grain and keys

- customers: one row per customer; primary key customer_id.
- sellers: one row per seller; primary key seller_id.
- products: one row per product/SKU; primary key product_id and unique SKU.
- sales: one row per sale line; primary key sale_id. It references one customer, seller, and product.

## Sales fields

- sale_date: ISO calendar date.
- quantity: units sold; must be greater than zero.
- unit_price: synthetic selling price per unit on the sale record.
- discount_rate: fraction from 0 to 1; for example 0.10 represents 10%.
- net_amount: quantity × unit_price × (1 − discount_rate), rounded to two decimals.

## Limitations

The dataset does not define a separate order header, so an average ticket calculated from sales rows is not necessarily an average order value. Gross margin is an estimate based on unit cost and does not include operating expenses, taxes, or other costs.
