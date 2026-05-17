CREATE OR REPLACE TABLE `project-839c799e-2b34-4fae-814.olist_staging.mart_daily_revenue` AS

SELECT
    DATE(order_purchase_timestamp) AS order_date,
    COUNT(DISTINCT order_id) AS total_orders,
    SUM(price) AS gmv,
    SAFE_DIVIDE(SUM(price), COUNT(DISTINCT order_id)) AS avg_order_value,
    COUNTIF(is_ontime = 1)   AS ontime_orders,
    COUNT(DISTINCT order_id) AS total_delivered_orders

FROM `project-839c799e-2b34-4fae-814.olist_staging.int_orders_enriched`
WHERE order_purchase_timestamp IS NOT NULL
GROUP BY DATE(order_purchase_timestamp)
ORDER BY order_date
