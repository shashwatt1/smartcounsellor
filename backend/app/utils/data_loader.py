import os
import glob
import pandas as pd
from functools import lru_cache
from app.config import config

# We use the centralized config so we can dynamically point to data inside AWS Lambda
DATA_DIR = config.DATA_PATH


@lru_cache(maxsize=1)
def load_josaa_data() -> pd.DataFrame:
    """
    Load all CSV files from the data directory and unify them into a single DataFrame.
    This handles multiple files like 'IIT_Open.csv', 'NIT.csv', 'Dataset - GFTI.csv', etc.
    """
    resolved_dir = os.path.normpath(DATA_DIR)
    csv_files = glob.glob(os.path.join(resolved_dir, "*.csv"))
    
    if not csv_files:
        raise FileNotFoundError(f"No CSV files found in {resolved_dir}")

    dfs = []
    for file in csv_files:
        try:
            # We skip lines with bad characters or extra rows if any
            df = pd.read_csv(file)
            
            # Normalise column names: strip whitespace, lowercase, replace spaces with underscores
            df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]
            
            dfs.append(df)
        except Exception as e:
            print(f"Warning: Failed to load {file} - {e}")
            
    if not dfs:
        raise ValueError("No valid data could be loaded from the CSV files.")

    combined_df = pd.concat(dfs, ignore_index=True)
    
    # We drop any completely empty rows that Excel/CSV might have appended
    combined_df.dropna(subset=['institute', 'closing_rank'], inplace=True)
    
    # Ensure closing and opening ranks are integers (coerce errors to nan, then drop)
    combined_df['closing_rank'] = pd.to_numeric(combined_df['closing_rank'], errors='coerce')
    combined_df['opening_rank'] = pd.to_numeric(combined_df['opening_rank'], errors='coerce')
    combined_df.dropna(subset=['closing_rank'], inplace=True)
    
    return combined_df
