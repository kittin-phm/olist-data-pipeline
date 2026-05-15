CREATE OR REPLACE VIEW `project-839c799e-2b34-4fae-814.olist_staging.vw_ontime_delivery_rate` AS
SELECT
    AVG(ontime_rate) * 100 AS avg_ontime_rate_pct
FROM `project-839c799e-2b34-4fae-814.olist_staging.mart_daily_revenue`