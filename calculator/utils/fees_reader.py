import pandas as pd
import logging
from .exceptions import ExcelFileReadError

def read_fees_data(file_path):
    try:
        fees_df = pd.read_excel(file_path)
    except FileNotFoundError:
        logging.error(f"File not found: {file_path}. Returning empty fees data.")
        return pd.DataFrame() 
    except Exception as e:
        logging.error(f"Error reading Excel file {file_path}: {e}. Returning empty fees data.")
        return pd.DataFrame() 

    if fees_df.empty:
        logging.warning(f"Fees data is empty in {file_path}")

    return fees_df
