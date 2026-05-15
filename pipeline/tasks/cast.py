import pandas as pd
import logging

logger = logging.getLogger(__name__)

def cast_orders(df: pd.DataFrame) -> pd.DataFrame:
    df['order_id'] = df['order_id'].astype(str)
    df['customer_id'] = df['customer_id'].astype(str)
    df['order_status'] = df['order_status'].astype(str)
    df['order_purchase_timestamp'] = pd.to_datetime(df['order_purchase_timestamp'])
    df['order_delivered_customer_date'] = pd.to_datetime(df['order_delivered_customer_date'], errors='coerce')
    df['order_estimated_delivery_date'] = pd.to_datetime(df['order_estimated_delivery_date'], errors='coerce')
    logger.info(f"Cast orders: {len(df)} rows")
    return df

def cast_order_items(df: pd.DataFrame) -> pd.DataFrame:
    df['order_id'] = df['order_id'].astype(str)
    df['product_id'] = df['product_id'].astype(str)
    df['seller_id'] = df['seller_id'].astype(str)
    df['price'] = df['price'].astype(float)
    df['freight_value'] = df['freight_value'].astype(float)
    logger.info(f"Cast order_items: {len(df)} rows")
    return df

def cast_payments(df: pd.DataFrame) -> pd.DataFrame:
    df['order_id'] = df['order_id'].astype(str)
    df['payment_type'] = df['payment_type'].astype(str)
    df['payment_value'] = df['payment_value'].astype(float)
    logger.info(f"Cast payments: {len(df)} rows")
    return df