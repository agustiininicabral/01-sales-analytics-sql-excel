# Sales Analytics Junior (SQL + Excel)

## Objetivo
Proyecto end-to-end: carga de datos (CSV) → modelo relacional → consultas SQL → dashboard en Excel con KPIs y gráficos.

## Stack
- SQL (PostgreSQL)
- Excel (Dashboard)
- Python (carga opcional con SQLAlchemy)
- Dataset sintético incluido

## Cómo ejecutar (rápido)
1) Crear tablas: ejecutar `sql/schema.sql`
2) (Opcional) Cargar datos: `python scripts/load_to_postgres.py --db <SQLALCHEMY_URL> --data data`
3) Ejecutar consultas: `sql/queries.sql`
4) Abrir `excel/dashboard_sales.xlsx`

## Estructura
```
01-sales-analytics-sql-excel/
├── data/ (CSVs)
├── excel/dashboard_sales.xlsx
├── sql/schema.sql
├── sql/queries.sql
└── scripts/load_to_postgres.py
```

## Notas
- El dashboard se alimenta desde la hoja `raw_sales` (ideal para simular un export desde SQL).
- Puedes reemplazar el dataset por datos reales sin cambiar la estructura.
