
# ttd_service/app/data_loader.py

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




def return_preprocessed_ttd(data_dir="data") -> dict[str, pl.DataFrame]:
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
    p = lambda *a: str(Path(data_dir, *a))
    f_ttd_download       = ensure_exists(p("P1-01-TTD_target_download.parquet"))
    f_ttd_drug           = ensure_exists(p("P1-02-TTD_drug_download.parquet"))
    f_ttd_drug_disease   = ensure_exists(p("P1-05-Drug_disease.parquet"))
    f_ttd_target_disease = ensure_exists(p("P1-06-Target_disease.parquet"))
    f_ttd_mapping        = ensure_exists(p("P1-07-Drug-TargetMapping.parquet"))
    f_biomarker_disease  = ensure_exists(p("P1-08-Biomarker_disease.parquet"))
    f_kegg_pathway       = ensure_exists(p("P4-01-Target-KEGGpathway_all.parquet"))
    f_ttd_disease        = ensure_exists(p("disease_master_table_ttd.parquet"))

    tasks = {
        "ttd_target_download":   lambda: read_parquet_polars(f_ttd_download),
        "ttd_drug_download":     lambda: read_parquet_polars(f_ttd_drug),
        "ttd_drug_disease":      lambda: read_parquet_polars(f_ttd_drug_disease),
        "ttd_target_disease":    lambda: read_parquet_polars(f_ttd_target_disease),
        "ttd_mapping":           lambda: read_parquet_polars(f_ttd_mapping),
        "ttd_biomarker_disease": lambda: read_parquet_polars(f_biomarker_disease),
        "ttd_kegg_pathway":      lambda: read_parquet_polars(f_kegg_pathway),
        "ttd_disease_download":  lambda: read_parquet_polars(f_ttd_disease),
    }
    results = {name: fn() for name, fn in tasks.items()}

    # Standardize column names
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

    for name, df in results.items():
        rename_dict = {c: mapping[c] for c in df.columns if c in mapping}
        if rename_dict:
            df = df.rename(rename_dict)
        # df = strip_all_whitespace(df).unique()
        df = df.unique()
        results[name] = df

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
