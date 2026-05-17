# 🛒 Olist E-Commerce Data Pipeline

> End-to-end data engineering project: ETL with Prefect → BigQuery DWH modeling → Power BI dashboard
> **Dataset**: Brazilian E-Commerce (Olist) from Kaggle · ~100,000 orders · Sep 2016 – Aug 2018

---

## 📁 Repository Structure

```
├── README.md
├── requirements.txt
├── .gitignore
├── pipelines/
│   ├── flow.py                  # @flow หลัก — orchestrates all tasks
│   └── tasks/                   # extract, cast, dq_check, load
├── sql/
│   ├── staging/                 # stg_orders, stg_order_items, stg_payments
│   ├── intermediate/            # int_orders_enriched
│   └── mart/                    # mart_daily_revenue + 3 KPI views
└── bi/
    ├── dashboard.pbix
    └── dax_measures.md
```

---

## Part 1 — ETL Pipeline & Orchestration

**Stack**: Python · Prefect v1 · BigQuery

### What it does

Ingests 3 CSV files from the Olist dataset into BigQuery staging tables using a Prefect-orchestrated pipeline with separate tasks for each concern:

| Task | Responsibility |
|---|---|
| `extract` | Read CSVs from local path |
| `cast` | Apply correct data types (no "everything is STRING") |
| `dq_check` | Validate data quality before load |
| `load` | Write to BigQuery staging tables |

### Staging Tables Created

- `stg_orders` — order-level data with proper timestamp types
- `stg_order_items` — item-level with numeric price/freight
- `stg_payments` — payment method and value per order

### How to Run

**1. Install dependencies**
```bash
py -3.11 -m pip install -r requirements.txt
```

**2. Authenticate with Google Cloud**
```bash
gcloud auth application-default login
```

**3. Run the pipeline**
```bash
py -3.11 pipelines/flow.py
```

The flow will log row counts at each stage and skip (not cancel) any rows that fail DQ checks.

### Data Quality Checks (pre-load)

| Check | Action on failure |
|---|---|
| `order_id` is null | Log warning + reject row |
| `customer_id` is null | Log warning + reject row |
| `price` ≤ 0 | Log warning + reject row |

> ✅ DQ failures do **not** cancel the entire flow — bad rows are skipped and counted in the log.

---

## Part 2 — DWH Modeling in BigQuery

**Stack**: SQL · Star Schema · BigQuery

### Layer Architecture

```
[Staging] → [Intermediate] → [Mart] → [KPI Views]
```

**Why not query staging directly?**
Staging holds raw data with no business logic. Separating layers means:
- Staging changes don't break downstream queries
- Business rules (join logic, metric definitions) live in one place
- BI tool only reads from mart — fast, pre-aggregated

### Intermediate Layer

**`int_orders_enriched`** — joins orders + items + payments

Key computed columns:
- `delivery_lead_time_days` = `order_delivered_customer_date` − `order_purchase_timestamp`
- `is_ontime` = 1 if delivered on or before `order_estimated_delivery_date`

### Mart Layer

**`mart_daily_revenue`** — daily aggregated GMV and order counts, consumed directly by Power BI

### KPI Views

| View | Definition |
|---|---|
| `vw_monthly_gmv` | SUM(price) grouped by year-month |
| `vw_avg_aov` | GMV / COUNT(distinct order_id) per month |
| `vw_ontime_rate` | % of delivered orders where `is_ontime = 1` |

---

## Part 3 — BI Dashboard & DAX

**Stack**: Power BI · DAX

### Dashboard 

Connected to BigQuery mart. Contains:
- 📈 **Monthly GMV trend** — line/bar chart, Sep 2016 – Aug 2018
- 💳 **Avg AOV card** — overall average order value across full dataset
- 🚚 **On-Time Delivery Rate card** — overall delivery performance
- 📅 **Date slicer** — filters all visuals by year_month simultaneously

### DAX Measures (`bi/dax_measures.md`)

**Why use DAX measures instead of pulling from mart directly?**
Calculated columns are static and stored in memory. DAX measures recalculate dynamically based on the active slicer context — essential for the date filter to affect AOV and On-Time Rate correctly.

```dax
-- Average Order Value
AOV = DIVIDE([Total GMV], [Total Orders])

-- On-Time Delivery Rate (responds to slicer)
On-time Delivery Rate % =
    DIVIDE(
        CALCULATE([Total Orders], mart_daily_revenue[is_ontime] = 1),
        [Total Orders]
    )
```

### KPI Results

| Metric | Value |
|---|---|
| Total GMV | 14.21M BRL |
| Avg AOV | 130.72 BRL |
| Avg On-Time Rate | ~85–90% per month |

---

## Data Quality & Null Strategy

Two null issues exist in this dataset by design — here's how each is handled:

### 1. `product_category_name` (~1,600 null rows)

**Why nulls exist**: Some products were not categorized in the source system.

**Strategy**: Retained as-is in staging. Filtered out in the intermediate layer using `WHERE product_category_name IS NOT NULL` only when category-level analysis is needed. Orders themselves are **not dropped** — revenue data is preserved.

### 2. `order_delivered_customer_date` (null for undelivered orders)

**Why nulls exist**: Orders still in transit or cancelled have no delivery date.

**Strategy**: Excluded from on-time delivery calculation by filtering `WHERE order_status = 'delivered'`. This ensures the metric only measures orders that actually completed delivery.

---

## BigQuery Project

```
Project : project-839c799e-2b34-4fae-814
Dataset : olist_staging
```

---

## Data Source

[Brazilian E-Commerce Public Dataset by Olist — Kaggle](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)

> CSV files are **not committed** to this repo. Download from Kaggle and place in the path referenced in `pipelines/tasks/extract.py`.

---

## Dashboard Preview

![Dashboard](bi/dashboard.png)
