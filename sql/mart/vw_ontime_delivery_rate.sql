-- vw_ontime_delivery_rate.sql
CREATE OR REPLACE VIEW `project-839c799e-2b34-4fae-814.olist_staging.vw_ontime_delivery_rate` AS
SELECT
    FORMAT_DATE('%Y-%m', order_date) AS year_month,
    SAFE_DIVIDE(SUM(ontime_orders), SUM(total_delivered_orders)) * 100 AS ontime_delivery_rate_pct
FROM `project-839c799e-2b34-4fae-814.olist_staging.mart_daily_revenue`
GROUP BY year_month
ORDER BY year_month
