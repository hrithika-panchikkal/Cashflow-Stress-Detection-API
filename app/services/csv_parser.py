import pandas as pd
from fastapi import UploadFile

from app.utils.constants import REQUIRED_COLUMNS
from app.services.data_cleaner import clean_transactions

async def parse_csv(
        file: UploadFile
) -> pd.DataFrame:
    """
    Parse uploaded CSV file
    and return cleaned dataframe.
    """
    try:
        # Read uploaded CSV file into dataframe
        df = pd.read_csv(file.file)
    except Exception as error:
        raise ValueError(
            f"Failed to read CSV file: {str(error)}"
        )
    
    # Normalize column names
    df.columns = [
        col.strip().lower()
        for col in df.columns
    ]

    # Validate required columns
    missing_columns = [
        column
        for column in REQUIRED_COLUMNS
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
    )

    # Clean malformed transaction data
    cleaned_df = clean_transactions(df)

    return cleaned_df

