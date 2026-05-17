# DAX Measures Documentation

All measures are defined on the `mart_daily_revenue` table.
Measures are used instead of calculated columns because they evaluate dynamically based on filter context (slicer, date filter), making them correct at any aggregation level.

---

## Total GMV

```dax
Total GMV = SUM(mart_daily_revenue[gmv])
```

Sums all daily GMV across the dataset. Result: **14.21M BRL**

---

## Avg AOV (Average Order Value)

```dax
Avg AOV =
    DIVIDE(
        SUM(mart_daily_revenue[gmv]),
        SUM(mart_daily_revenue[total_orders])
    )
```

Weighted average — total revenue divided by total orders. Result: **142.89 BRL**

Using `DIVIDE()` instead of `/` to safely handle division by zero.

---

## Avg Ontime Rate %

```dax
Avg Ontime Rate % =
    DIVIDE(
        SUMX(ALL(mart_daily_revenue), mart_daily_revenue[ontime_orders]),
        SUMX(ALL(mart_daily_revenue), mart_daily_revenue[total_delivered_orders])
    ) * 100
```

Weighted on-time rate — total on-time deliveries divided by total delivered orders. Result: **92.15%**

Verified against BigQuery: 106,004 on-time ÷ 115,038 delivered = 92.15%

### Why not AVERAGE(ontime_rate)?

An early version stored `AVG(is_ontime)` as a pre-calculated float per day, then used `AVERAGE()` in DAX. This inflated the result to **106%** because early months (Sep–Nov 2016) had very few orders but near-perfect delivery — small-volume days were weighted equally to high-volume days.

The fix: store raw `ontime_orders` and `total_delivered_orders` counts in the mart, then use `DIVIDE(SUM(...), SUM(...))` for a properly weighted rate.
