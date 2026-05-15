import pandas as pd
import logging

logger = logging.getLogger(__name__)

def extract_csv(file_path: str) -> pd.DataFrame:
    df = pd.read_csv(file_path)
    logger.info(f"Extracted {len(df)} rows from {file_path}")
    return df
