# DAX Measures

All measures are defined on the `mart_daily_revenue` table.
Measures are used instead of calculated columns because they evaluate dynamically based on filter context (slicer, date filter) — pulling values directly from the mart without storing redundant data row-by-row.

---

## Measure 1 — AOV (Average Order Value)

```dax
Avg AOV =
    DIVIDE(
        SUM(mart_daily_revenue[gmv]),
        SUM(mart_daily_revenue[total_orders])
    )
```

**Why this formula:**
- `DIVIDE()` is used instead of `/` to safely handle division by zero (returns BLANK instead of error)
- Pulls `gmv` and `total_orders` directly from `mart_daily_revenue` — no intermediate calculation needed
- Responds dynamically to the `year_month` slicer — filters automatically narrow the SUM range

**Result:** 142.89 BRL

---

## Measure 2 — On-time Delivery Rate %

```dax
Avg Ontime Rate % =
    DIVIDE(
        SUM(mart_daily_revenue[ontime_orders]),
        SUM(mart_daily_revenue[total_delivered_orders])
    ) * 100
```

**Why this formula:**
- Uses raw counts (`ontime_orders`, `total_delivered_orders`) stored in the mart — not a pre-averaged float
- `SUM / SUM` gives a properly weighted rate across any date range selected by the slicer
- Multiplied by 100 to display as percentage (e.g. 92.15 instead of 0.9215)
- Responds to the `year_month` slicer — when a month is selected, only that month's counts are summed

**Why not `AVERAGE(ontime_rate)`:**
An earlier version stored `AVG(is_ontime)` as a pre-calculated float per day and used `AVERAGE()` in DAX. This inflated the result to **106%** because early months (Sep–Nov 2016) had very few orders but near-perfect delivery — small-volume days were weighted equally to high-volume days. Storing raw counts and using `DIVIDE(SUM, SUM)` fixes this.

**Result:** 92.15% — verified against BigQuery (106,004 on-time ÷ 115,038 delivered)
