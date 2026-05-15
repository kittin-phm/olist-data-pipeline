import logging
from google.cloud import bigquery

logger = logging.getLogger(__name__)

def load_to_bigquery(df, table_name: str, project_id: str, dataset_id: str):
    client = bigquery.Client(project=project_id)
    table_ref = f"{project_id}.{dataset_id}.{table_name}"
    
    job_config = bigquery.LoadJobConfig(
        write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE
    )
    
    job = client.load_table_from_dataframe(df, table_ref, job_config=job_config)
    job.result()  # Wait until done
    
    logger.info(f"Loaded {len(df)} rows to {table_ref}")
    print(f"✅ Loaded {len(df)} rows to {table_ref}")