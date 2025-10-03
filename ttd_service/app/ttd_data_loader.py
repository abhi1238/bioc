# ttd_service/app/data_loader.py

import polars as pl
from pathlib import Path
import logging
from os import getcwd
import os
from polars import col, String 


def get_fallback_logger(name="biochirp.tmp"):
    """
    Return a logger instance for the given name, ensuring logging is always available.

    If no root logger handlers are set (e.g., the app is run as a standalone script or test),
    this function will automatically configure a basic console logger with INFO level.
    This ensures that logs are never lost, whether or not a global logging setup exists.

    Args:
        name (str): The name of the logger to retrieve. Use a module- or component-specific
                    string for easier log filtering. Defaults to "biochirp.tmp".

    Returns:
        logging.Logger: Configured logger instance, ready for use.

    Example:
        >>> from app.utils.logger import get_fallback_logger
        >>> logger = get_fallback_logger("biochirp.services")
        >>> logger.info("Logger is ready!")
    """
    logger = logging.getLogger(name)
    if not logging.getLogger().hasHandlers():
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
        )
    return logger

def ensure_exists(filename: str, data_dir="data") -> str:
    """
    Check if a file exists in the given data_dir or at an absolute path.

    Args:
        filename (str): Filename (not full path).
        data_dir (str): Relative or absolute directory where to look for the file.

    Returns:
        str: Absolute path if the file exists.

    Raises:
        FileNotFoundError: If the file does not exist, with diagnostics.
    """
    # Prefer Path for everything

    try:
    # Script mode: use file path
        PROJECT_ROOT = Path(__file__).resolve().parents[1]
    except NameError:
        # Notebook mode: use cwd, then go up two parents (like parents[2])
        PROJECT_ROOT = Path(os.getcwd()).resolve().parents[1]

    file_path = Path(PROJECT_ROOT)/ data_dir / filename

    file_path = Path(file_path).resolve()

    try:
        if not file_path.exists():
            raise FileNotFoundError
        return str(file_path)
    except Exception as e:
        msg = (
            f"File not found: '{file_path}'\n"
            f"  Current working directory: {getcwd()}\n"
            f"  Searched for file at: {file_path}\n"
            f"  Exception: {e.__class__.__name__}: {e}\n"
            "  TIP: Double-check your relative path and working directory."
        )
        raise FileNotFoundError(msg)


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



# def strip_all_whitespace(df):
#     """
#     Strip leading and trailing whitespace from all string columns in a Polars DataFrame.

#     Args:
#         df (pl.DataFrame): Input DataFrame.

#     Returns:
#         pl.DataFrame: DataFrame with all string columns stripped of whitespace.
#     """
#     for col in df.columns:
#         if pl.datatypes.is_string_dtype(df[col].dtype):
#             df = df.with_columns(pl.col(col).str.strip())
#     return df

def strip_all_whitespace(df: pl.DataFrame) -> pl.DataFrame:
    """
    Strip leading and trailing whitespace from all string columns in a Polars DataFrame.

    Args:
        df (pl.DataFrame): Input DataFrame.

    Returns:
        pl.DataFrame: DataFrame with all string columns stripped of whitespace.
    """
    # Fix: Use a vectorized approach to apply the strip operation
    # to ALL string columns in a single, efficient operation.
    return df.with_columns(
    # Select all columns with the Utf8 (string) data type
    pl.col(pl.Utf8).str.strip()  # Corrected: Use .str.strip()
)



def return_preprocessed_ttd(data_dir="data", logger=None) -> dict[str, pl.DataFrame]:
    """
    Load and preprocess all TTD (Therapeutic Target Database) Parquet tables from the specified data directory.

    This function:
        - Ensures the existence of all required TTD Parquet files.
        - Reads each file into a Polars DataFrame.
        - Standardizes column names across all tables for downstream consistency.
        - Strips leading/trailing whitespace from all string columns and deduplicates rows.
        - Returns a dictionary mapping canonical table names to Polars DataFrames.

    Args:
        data_dir (str, optional): Directory containing the TTD Parquet files. Defaults to "data".

    Returns:
        dict[str, pl.DataFrame]: Dictionary with standardized table names as keys and processed Polars DataFrames as values.

    Raises:
        FileNotFoundError: If any required Parquet file is missing.

    Example:
        >>> tables = return_preprocessed_ttd("/app/data")
        >>> tables["drug_master_table_ttd"].head()

    Canonical keys returned:
        - "target_master_table_ttd"
        - "drug_master_table_ttd"
        - "drug_disease_association_ttd"
        - "target_disease_association_ttd"
        - "drug_target_association_ttd"
        - "biomarker_disease_association_ttd"
        - "target_pathway_association_ttd"
        - "disease_master_table_ttd"
    """


    if logger is None:
        logger = get_fallback_logger()

    try:
        logger.info("[TTD] Started loading TTD database...")

        f_ttd_download       = ensure_exists("P1-01-TTD_target_download.parquet")
        f_ttd_drug           = ensure_exists("P1-02-TTD_drug_download.parquet")
        f_ttd_drug_disease   = ensure_exists("P1-05-Drug_disease.parquet")
        f_ttd_target_disease = ensure_exists("P1-06-Target_disease.parquet")
        f_ttd_mapping        = ensure_exists("P1-07-Drug-TargetMapping.parquet")
        f_biomarker_disease  = ensure_exists("P1-08-Biomarker_disease.parquet")
        f_kegg_pathway       = ensure_exists("P4-01-Target-KEGGpathway_all.parquet")
        f_ttd_disease        = ensure_exists("disease_master_table_ttd.parquet")
        
        tasks = {
            "ttd_target_download":   read_parquet_polars(f_ttd_download),
            "ttd_drug_download":     read_parquet_polars(f_ttd_drug),
            "ttd_drug_disease":      read_parquet_polars(f_ttd_drug_disease),
            "ttd_target_disease":    read_parquet_polars(f_ttd_target_disease),
            "ttd_mapping":           read_parquet_polars(f_ttd_mapping),
            "ttd_biomarker_disease": read_parquet_polars(f_biomarker_disease),
            "ttd_kegg_pathway":      read_parquet_polars(f_kegg_pathway),
            "ttd_disease_download":  read_parquet_polars(f_ttd_disease),
        }

        # print(tasks)

        mapping = {
            "DRUG_NAME": "drug_name", "Drug_Name": "drug_name",
            "GENE_SYMBOL": "gene_name", "Target": "gene_name",
            "Disease_Name": "disease_name", "# Disease_Name": "disease_name",
            "PathwayID": "pathway_id", "PATH_NAME": "pathway_name", "path_name": "pathway_name",
            "Pubchem_CID": "PUBCHEM_CID",
            "Biomarker_Name": "biomarker_name",
            "TTDID": "target_id", "KEGG pathway ID": "pathway_id",
            "KEGG pathway name": "pathway_name",
            "TargetID": "target_id", "DrugID": "drug_id",
            "MOA": 'drug_mechanism_of_action_on_target'
        }

        results = dict()

        # print("hi")

        for name, df in tasks.items():
            rename_dict = {c: mapping[c] for c in df.columns if c in mapping}
            if rename_dict:
                df = df.rename(rename_dict)


            # df = strip_all_whitespace(df).unique()
            df = df.unique()
            results[name] = df

        logger.info("[TTD] Finished  loading TTD database...")

        return {
            "target_master_table_ttd": results["ttd_target_download"],
            "drug_master_table_ttd": results["ttd_drug_download"],
            "drug_disease_association_ttd": results["ttd_drug_disease"],
            "target_disease_association_ttd": results["ttd_target_disease"],
            "drug_target_association_ttd": results["ttd_mapping"],
            "biomarker_disease_association_ttd": results["ttd_biomarker_disease"],
            "target_pathway_association_ttd": results["ttd_kegg_pathway"],
            "disease_master_table_ttd": results["ttd_disease_download"],
        }
    
    except:

        logger.error("[TTD] Error loading TTD database...")
