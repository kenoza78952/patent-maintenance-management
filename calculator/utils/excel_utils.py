import pandas as pd
import logging
from .exceptions import MissingRequiredColumnsError

def read_patent_data(file_path):
    try:
        full_df = pd.read_excel(file_path)
    except FileNotFoundError:
        logging.error(f"File not found: {file_path}")
        raise
    except Exception as e:
        logging.error(f"Error reading Excel file {file_path}: {e}")
        raise

    necessary_columns = [
        'Patent/ Publication Number', 
        'Publication Country', 
        'Type', 
        'File Date', 
        'Publication Date', 
        'Est. Expiration Date', 
        'Number of claims'
    ]

    missing_columns = [col for col in necessary_columns if col not in full_df.columns]
    if missing_columns:
        raise MissingRequiredColumnsError(missing_columns, necessary_columns)

    processed_df = full_df[necessary_columns].copy()
    return full_df, processed_df


def extract_patent_info(patent_df):
    patent_info = []

    for index, row in patent_df.iterrows():
        patent_number = row['Patent/ Publication Number'] 
        country = row['Publication Country']
        type = row['Type']
        filing_date = row['File Date'] 
        issued_date = row['Publication Date']
        expiration_date = row['Est. Expiration Date'] 
        numofclaims = row['Number of claims']


        patent_info.append((patent_number, type, filing_date, issued_date, expiration_date, country, numofclaims))

    return patent_info
