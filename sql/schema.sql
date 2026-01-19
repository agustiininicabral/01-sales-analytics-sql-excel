-- DB: PostgreSQL (compatible con la mayoría de motores SQL con cambios mínimos)
CREATE TABLE IF NOT EXISTS dim_customer (
  customer_id   INT PRIMARY KEY,
  customer_name TEXT NOT NULL,
  city          TEXT NOT NULL,
  segment       TEXT NOT NULL,
  signup_date   DATE NOT NULL
);

CREATE TABLE IF NOT EXISTS dim_seller (
  seller_id   INT PRIMARY KEY,
  seller_name TEXT NOT NULL,
  team        TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS dim_product (
  product_id   INT PRIMARY KEY,
  sku          TEXT NOT NULL UNIQUE,
  product_name TEXT NOT NULL,
  category     TEXT NOT NULL,
  unit_cost    NUMERIC(10,2) NOT NULL,
  unit_price   NUMERIC(10,2) NOT NULL
);

CREATE TABLE IF NOT EXISTS fact_sale (
  sale_id       INT PRIMARY KEY,
  sale_date     DATE NOT NULL,
  customer_id   INT NOT NULL REFERENCES dim_customer(customer_id),
  seller_id     INT NOT NULL REFERENCES dim_seller(seller_id),
  product_id    INT NOT NULL REFERENCES dim_product(product_id),
  quantity      INT NOT NULL CHECK (quantity > 0),
  unit_price    NUMERIC(10,2) NOT NULL,
  discount_rate NUMERIC(5,2) NOT NULL CHECK (discount_rate >= 0 AND discount_rate <= 1),
  net_amount    NUMERIC(12,2) NOT NULL CHECK (net_amount >= 0)
);

CREATE INDEX IF NOT EXISTS idx_fact_sale_date ON fact_sale(sale_date);
CREATE INDEX IF NOT EXISTS idx_fact_sale_customer ON fact_sale(customer_id);
CREATE INDEX IF NOT EXISTS idx_fact_sale_product ON fact_sale(product_id);