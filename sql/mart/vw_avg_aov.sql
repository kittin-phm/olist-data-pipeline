CREATE OR REPLACE VIEW `project-839c799e-2b34-4fae-814.olist_staging.vw_avg_aov` AS
SELECT
    SAFE_DIVIDE(SUM(gmv), SUM(total_orders)) AS avg_aov
FROM `project-839c799e-2b34-4fae-814.olist_staging.mart_daily_revenue`
