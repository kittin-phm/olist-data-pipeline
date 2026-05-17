# Olist E-Commerce Data Pipeline

End-to-end data pipeline for the [Brazilian E-Commerce (Olist) dataset](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce) covering ~100,000 orders from Sep 2016 to Aug 2018.

---

## Architecture Overview

```
Kaggle CSV Files
      │
      ▼
[Part 1] Prefect ETL Pipeline
  Extract → Cast → DQ Check → Load
      │
      ▼
[Part 2] BigQuery Data Warehouse
  Staging → Intermediate → Mart → KPI Views
      │
      ▼
[Part 3] Power BI Dashboard
  DAX Measures → KPI Cards → Time-series Charts
```

---

## Part 1 — ETL Pipeline & Orchestration (Prefect)

### Stack
- **Orchestrator:** Prefect
- **Language:** Python 3.10+
- **Destination:** Google BigQuery

### Pipeline Flow

```
extract_data()
    └── cast_types()
          └── run_dq_checks()
                └── load_to_bigquery()
```

### Data Quality Rules

| Check | Rule | Action |
|-------|------|--------|
| Null order_id | `order_id IS NOT NULL` | Reject row |
| Negative price | `price >= 0` | Reject row |
| Null product_category | Allow null | Keep row — revenue still valid |
| Null delivered date | Allow null | Keep row — not yet delivered ≠ late |

### Data Quality Findings

**Finding 1 — Null `product_category_name`**
Some products have no category label. These rows were **kept** intentionally — dropping them would undercount revenue. The missing category is handled in the intermediate layer with a fallback label (`'unknown'`).

**Finding 2 — Null `order_delivered_customer_date`**
Orders that haven't been delivered yet have a null delivery date. These were **excluded only from on-time rate calculations** using `WHERE order_status = 'delivered'`. A null delivery date does not mean a late delivery — treating it as late would inflate the failure rate incorrectly.

---

## Part 2 — DWH Modeling in BigQuery

### Layer Design

```
olist_staging/
├── stg_orders              ← raw orders, cast + cleaned
├── stg_order_items         ← raw items, cast + cleaned
├── stg_products            ← raw products, null category handled
├── int_orders_enriched     ← joined orders + items + products
├── mart_daily_revenue      ← daily aggregated mart table
├── vw_aov                  ← view: average order value by month
├── vw_monthly_gmv          ← view: GMV by month
└── vw_ontime_delivery      ← view: on-time delivery rate by month
```

### Mart Table: `mart_daily_revenue`

| Column | Type | Description |
|--------|------|-------------|
| `order_date` | DATE | Purchase date |
| `total_orders` | INT | Count of distinct orders |
| `gmv` | FLOAT | Gross Merchandise Value (sum of price) |
| `avg_order_value` | FLOAT | GMV / total_orders per day |
| `ontime_orders` | INT | Delivered orders where delivered ≤ estimated |
| `total_delivered_orders` | INT | Total orders with status = 'delivered' |

### On-Time Rate Calculation

```sql
COUNTIF(
    order_status = 'delivered'
    AND order_delivered_customer_date <= order_estimated_delivery_date
) AS ontime_orders,
COUNTIF(order_status = 'delivered') AS total_delivered_orders
```

Using raw counts (not pre-averaged floats) ensures correct weighted aggregation at any granularity.

---

## Part 3 — BI Dashboard & DAX

### Dashboard KPIs (verified against BigQuery)

| KPI | Value | DAX Measure |
|-----|-------|-------------|
| Total GMV | 14.21M BRL | `SUM(mart_daily_revenue[gmv])` |
| Avg AOV | 142.89 BRL | `DIVIDE(SUM(gmv), SUM(total_orders))` |
| On-Time Delivery Rate | 92.15% | `DIVIDE(SUM(ontime_orders), SUM(total_delivered_orders)) * 100` |

### DAX Measures

```dax
Total GMV = SUM(mart_daily_revenue[gmv])

Avg AOV =
    DIVIDE(
        SUM(mart_daily_revenue[gmv]),
        SUM(mart_daily_revenue[total_orders])
    )

Avg Ontime Rate % =
    DIVIDE(
        SUMX(ALL(mart_daily_revenue), mart_daily_revenue[ontime_orders]),
        SUMX(ALL(mart_daily_revenue), mart_daily_revenue[total_delivered_orders])
    ) * 100
```

### Why Measures, Not Calculated Columns

DAX **measures** are used instead of calculated columns because:
- Measures evaluate dynamically based on filter context (slicer, date filter)
- Calculated columns are computed at refresh time and stored row-by-row — inefficient for aggregations
- `DIVIDE()` is used over `/` to safely handle division by zero

### Why Not AVERAGE(ontime_rate)?

An early version stored `AVG(is_ontime)` as a pre-calculated float per day, then used `AVERAGE()` in DAX. This inflated the result to **106%** because early months (Sep–Nov 2016) had very few orders but near-perfect delivery, so small-volume days were weighted equally to high-volume days.

The fix: store raw `ontime_orders` and `total_delivered_orders` counts in the mart, then use `DIVIDE(SUM(...), SUM(...))` for a properly weighted rate. BigQuery verification: 106,004 on-time ÷ 115,038 delivered = **92.15%**.

### Charts
- **Monthly Revenue (GMV)** — line chart, `year_month` × `SUM(monthly_gmv)`
- **Average Order Value (AOV)** — line chart, `year_month` × `SUM(aov)`
- **On-Time Delivery Rate %** — bar chart, `year_month` × `SUM(ontime_delivery_rate_pct)`

---

## Project Structure

```
olist-data-pipeline/
├── pipelines/
│   ├── flow.py               # Prefect main flow
│   └── tasks/                # extract, cast, dq, load tasks
├── sql/
│   ├── staging/              # stg_orders, stg_order_items, stg_products
│   ├── intermediate/         # int_orders_enriched
│   └── mart/                 # mart_daily_revenue, KPI views
├── bi/
│   ├── dashboard.pbix        # Power BI dashboard
│   └── dax_measures.md       # DAX formulas documentation
├── requirements.txt
└── README.md
```

---

## Setup

```bash
pip install -r requirements.txt
python pipelines/flow.py
```

Requires a `GOOGLE_APPLICATION_CREDENTIALS` environment variable pointing to a BigQuery service account JSON key.

---

## Data Source

[Brazilian E-Commerce Public Dataset by Olist](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce) — Kaggle, licensed under CC BY-NC-SA 4.0.
