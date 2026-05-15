import logging

logger = logging.getLogger(__name__)

def dq_check_orders(df):
    initial_rows = len(df)
    
    # Check null in order_id and customer_id
    null_mask = df['order_id'].isnull() | df['customer_id'].isnull()
    rejected = null_mask.sum()
    
    if rejected > 0:
        logger.warning(f"Rejected {rejected} rows with null order_id or customer_id")
    
    df = df[~null_mask]
    logger.info(f"Orders DQ: {initial_rows} in, {len(df)} passed, {rejected} rejected")
    return df

def dq_check_order_items(df):
    initial_rows = len(df)
    
    # Check null order_id and price > 0
    null_mask = df['order_id'].isnull()
    price_mask = df['price'] <= 0
    bad_mask = null_mask | price_mask
    rejected = bad_mask.sum()
    
    if rejected > 0:
        logger.warning(f"Rejected {rejected} rows with null order_id or price <= 0")
    
    df = df[~bad_mask]
    logger.info(f"Order_items DQ: {initial_rows} in, {len(df)} passed, {rejected} rejected")
    return df

def dq_check_payments(df):
    initial_rows = len(df)
    
    # Check null order_id
    null_mask = df['order_id'].isnull()
    rejected = null_mask.sum()
    
    if rejected > 0:
        logger.warning(f"Rejected {rejected} rows with null order_id")
    
    df = df[~null_mask]
    logger.info(f"Payments DQ: {initial_rows} in, {len(df)} passed, {rejected} rejected")
    return df