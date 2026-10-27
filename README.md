# Sales Analytics Junior — SQL + Excel

Proyecto de portfolio que conecta datos CSV sintéticos, un modelo relacional en PostgreSQL, consultas SQL de negocio y un dashboard de Excel.

![Data quality CI](https://github.com/agustiininicabral/01-sales-analytics-sql-excel/actions/workflows/ci.yml/badge.svg)

## Objetivo

Demostrar un flujo de análisis de ventas: validar fuentes, cargar dimensiones y hechos, calcular ingresos y márgenes, explorar clientes/productos y presentar KPIs en Excel.

**Datos:** todos los registros son ficticios; no representan una empresa ni una moneda real.

## Dataset

- `data/customers.csv`: clientes, ciudad, segmento y fecha de alta.
- `data/products.csv`: catálogo, categoría, costo y precio.
- `data/sellers.csv`: vendedores y equipo.
- `data/sales.csv`: ventas, fecha, cliente, vendedor, producto, cantidad, descuento e importe neto.
- `excel/dashboard_sales.xlsx`: dashboard de Excel de demostración.

El modelo de datos y la granularidad están documentados en [data/DATA_DICTIONARY.md](data/DATA_DICTIONARY.md).

## Validación local

Requiere Python 3.12 o posterior. La validación y sus pruebas usan la biblioteca estándar:

```powershell
python scripts/validate_data.py
python -m unittest discover -s tests -v
```

El validador comprueba columnas, IDs únicos, relaciones entre clientes/productos/vendedores, fechas, cantidades, precios, descuentos y reconciliación de net_amount con cantidad × precio × (1 − descuento). Genera `reports/data_quality_report.json`.

GitHub Actions ejecuta las pruebas y publica el reporte de calidad como artefacto temporal.

## Modelo SQL

1. Crear una base de datos PostgreSQL vacía.
2. Ejecutar [sql/schema.sql](sql/schema.sql).
3. Cargar los CSV si querés consultar los datos desde PostgreSQL.
4. Ejecutar [sql/queries.sql](sql/queries.sql).

Para usar el cargador opcional, instalar las dependencias:

```powershell
python -m pip install -r requirements.txt
```

Definí la variable de entorno `DATABASE_URL` con tu URL de SQLAlchemy y ejecutá:

```powershell
python scripts/load_to_postgres.py --db $env:DATABASE_URL --data data
```

El cargador agrega filas a tablas existentes; usalo sobre una base vacía o limpia las tablas antes de repetir la carga. No guardes contraseñas ni URLs privadas en el repositorio.

## Consultas incluidas

- Ventas netas por mes.
- Top 10 productos por ingresos netos.
- Ticket promedio por registro y unidades promedio por registro.
- Clientes con cinco o más compras.
- Margen bruto estimado por categoría.

La métrica de ticket es un promedio por fila de venta, no necesariamente por orden completa. El dashboard de Excel usa la hoja `raw_sales` y es un artefacto de demostración; la carga a PostgreSQL es opcional.

## Estructura

- `data/`: CSV sintéticos.
- `sql/schema.sql`: dimensiones, hechos, restricciones e índices.
- `sql/queries.sql`: consultas analíticas.
- `scripts/load_to_postgres.py`: carga opcional a PostgreSQL.
- `scripts/validate_data.py`: validación de calidad.
- `tests/test_validate_data.py`: pruebas de reglas y casos inválidos.
- `excel/dashboard_sales.xlsx`: dashboard de ejemplo.

## Licencia

MIT. Consultá [LICENSE](LICENSE).
