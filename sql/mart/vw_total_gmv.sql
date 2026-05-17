-- vw_total_gmv.sql
CREATE OR REPLACE VIEW `project-839c799e-2b34-4fae-814.olist_staging.vw_total_gmv` AS
SELECT
    FORMAT_DATE('%Y-%m', order_date) AS year_month,
    SUM(gmv) AS total_gmv
FROM `project-839c799e-2b34-4fae-814.olist_staging.mart_daily_revenue`
GROUP BY year_month
ORDER BY year_month
