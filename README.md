# Olist E-Commerce Data Pipeline

## Project Structure
- `pipeline/` - Prefect ETL pipeline (extract, cast, DQ check, load)
- `sql/` - BigQuery SQL models (staging, intermediate, mart, KPI views)
- `bi/` - Power BI dashboard and DAX measures

## Setup

### 1. Install dependencies
```bash
py -3.11 -m pip install -r requirements.txt
```

### 2. Authenticate with Google Cloud
```bash
gcloud auth application-default login
```

### 3. Run the pipeline
```bash
py -3.11 pipeline/flow.py
```

## BigQuery Dataset
Project: `project-839c799e-2b34-4fae-814`  
Dataset: `olist_staging`

## Data Quality & Null Strategy
- **product_category_name**: ~1,600 null rows retained as-is in staging; filtered downstream
- **order_delivered_customer_date**: null for undelivered orders; excluded from on-time delivery calculation using `WHERE order_status = 'delivered'`
- Null `order_id` and negative `price` rows are rejected in DQ check layer

## Data Source
[Brazilian E-Commerce Dataset - Kaggle](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)

## Dashboard Preview
![Dashboard](bi/dashboard.png)

## Dashboard Description

This Power BI dashboard analyzes **Olist Brazilian E-Commerce** transaction data 
covering the period **September 2016 to August 2018** (~100,000 orders).

### KPI Cards
- **Total GMV**: 14.21M BRL — total gross merchandise value across all orders
- **Avg AOV**: 130.72 BRL — average revenue per order
- **Avg On-Time Rate**: ~86% — percentage of orders delivered on or before estimated date

### Charts
- **Monthly Revenue (GMV)**: Revenue trend by month — shows peak in late 2017 and gradual decline toward mid-2018
- **Average Order Value (AOV)**: AOV trend by month — relatively stable around 140-160 BRL throughout the period
- **On-Time Delivery Rate %**: Consistent delivery performance (~85-90%) across all months with minor fluctuations

### Slicer
- **year_month filter**: Allows filtering all visuals by specific month for drill-down analysis

### DAX Measures
- `Total GMV` — SUM of monthly GMV
- `Avg AOV` — AVERAGE of monthly AOV
- `Avg Ontime Rate` — AVERAGE of monthly on-time delivery rate