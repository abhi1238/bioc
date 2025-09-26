# biochirp/common_utils/loader_utils.py

import polars as pl
from pathlib import Path

def ensure_exists(path):
    """
    Check if a file exists at the given path.

    Args:
        path (str or Path): Path to the file.

    Returns:
        str or Path: The same path if the file exists.

    Raises:
        FileNotFoundError: If the file does not exist.
    """
    if not Path(path).exists():
        raise FileNotFoundError(f"{path} not found!")
    return path

def read_parquet_polars(path, name=None):
    """
    Load a Parquet file as a Polars DataFrame.

    Args:
        path (str or Path): Path to the Parquet file.
        name (str, optional): Not used, for API compatibility.

    Returns:
        pl.DataFrame: Loaded Polars DataFrame.
    """
    return pl.read_parquet(path)

def strip_all_whitespace(df):
    """
    Strip leading and trailing whitespace from all string columns in a Polars DataFrame.

    Args:
        df (pl.DataFrame): Input DataFrame.

    Returns:
        pl.DataFrame: DataFrame with all string columns stripped of whitespace.
    """
    for col in df.columns:
        if pl.datatypes.is_string_dtype(df[col].dtype):
            df = df.with_columns(pl.col(col).str.strip())
    return df
