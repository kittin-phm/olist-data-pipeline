-- vw_avg_aov.sql
CREATE OR REPLACE VIEW `project-839c799e-2b34-4fae-814.olist_staging.vw_avg_aov` AS
SELECT
    FORMAT_DATE('%Y-%m', order_date) AS year_month,
    SAFE_DIVIDE(SUM(gmv), SUM(total_orders)) AS avg_aov
FROM `project-839c799e-2b34-4fae-814.olist_staging.mart_daily_revenue`
GROUP BY year_month
ORDER BY year_month
