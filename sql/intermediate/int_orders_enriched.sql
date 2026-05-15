CREATE OR REPLACE TABLE `project-839c799e-2b34-4fae-814.olist_staging.int_orders_enriched` AS

SELECT
    o.order_id,
    o.customer_id,
    o.order_status,
    o.order_purchase_timestamp,
    o.order_delivered_customer_date,
    o.order_estimated_delivery_date,
    
    -- Items info
    i.product_id,
    i.seller_id,
    i.price,
    i.freight_value,
    
    -- Payment info
    p.payment_type,
    p.payment_value,
    
    -- Calculate delivery lead time in days
    DATE_DIFF(
        DATE(o.order_delivered_customer_date),
        DATE(o.order_purchase_timestamp),
        DAY
    ) AS delivery_lead_time_days

FROM `project-839c799e-2b34-4fae-814.olist_staging.stg_orders` o
LEFT JOIN `project-839c799e-2b34-4fae-814.olist_staging.stg_order_items` i
    ON o.order_id = i.order_id
LEFT JOIN `project-839c799e-2b34-4fae-814.olist_staging.stg_payments` p
    ON o.order_id = p.order_id