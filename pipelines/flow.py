import logging
import sys
from prefect import flow, task

sys.path.append('C:\\olist_project')

from pipeline.tasks.extract import extract_csv
from pipeline.tasks.cast import cast_orders, cast_order_items, cast_payments
from pipeline.tasks.dq_check import dq_check_orders, dq_check_order_items, dq_check_payments
from pipeline.tasks.load import load_to_bigquery

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Config
PROJECT_ID = "project-839c799e-2b34-4fae-814"
DATASET_ID = "olist_staging"
DATA_PATH = "C:\\olist_project\\data\\"

@task
def process_orders():
    df = extract_csv(DATA_PATH + "olist_orders_dataset.csv")
    df = cast_orders(df)
    df = dq_check_orders(df)
    load_to_bigquery(df, "stg_orders", PROJECT_ID, DATASET_ID)

@task
def process_order_items():
    df = extract_csv(DATA_PATH + "olist_order_items_dataset.csv")
    df = cast_order_items(df)
    df = dq_check_order_items(df)
    load_to_bigquery(df, "stg_order_items", PROJECT_ID, DATASET_ID)

@task
def process_payments():
    df = extract_csv(DATA_PATH + "olist_order_payments_dataset.csv")
    df = cast_payments(df)
    df = dq_check_payments(df)
    load_to_bigquery(df, "stg_payments", PROJECT_ID, DATASET_ID)

@flow(name="olist-etl-pipeline")
def main_flow():
    logger.info("Starting Olist ETL Pipeline...")
    process_orders()
    process_order_items()
    process_payments()
    logger.info("Pipeline completed!")

if __name__ == "__main__":
    main_flow()