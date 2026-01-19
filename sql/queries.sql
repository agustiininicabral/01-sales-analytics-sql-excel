-- 1) Ventas netas por mes
SELECT date_trunc('month', sale_date)::date AS month,
       SUM(net_amount) AS net_sales
FROM fact_sale
GROUP BY 1
ORDER BY 1;

-- 2) Top 10 productos por ventas netas
SELECT p.product_name, p.category, SUM(s.net_amount) AS net_sales
FROM fact_sale s
JOIN dim_product p ON p.product_id = s.product_id
GROUP BY 1,2
ORDER BY net_sales DESC
LIMIT 10;

-- 3) Ticket promedio y unidades promedio por transacción
SELECT AVG(net_amount) AS avg_ticket,
       AVG(quantity)   AS avg_units
FROM fact_sale;

-- 4) Clientes recurrentes (>= 5 compras)
SELECT c.customer_name, COUNT(*) AS purchases, SUM(s.net_amount) AS net_sales
FROM fact_sale s
JOIN dim_customer c ON c.customer_id = s.customer_id
GROUP BY 1
HAVING COUNT(*) >= 5
ORDER BY net_sales DESC;

-- 5) Margen estimado por categoría (precio - costo) * unidades
SELECT p.category,
       SUM((p.unit_price - p.unit_cost) * s.quantity) AS est_gross_margin
FROM fact_sale s
JOIN dim_product p ON p.product_id = s.product_id
GROUP BY 1
ORDER BY est_gross_margin DESC;