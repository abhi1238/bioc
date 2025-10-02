
# import os
# import time
# from concurrent.futures import ThreadPoolExecutor, as_completed
# from pathlib import Path
# from typing import Callable, Dict, Iterable, Tuple
# import polars as pl


# try:
#     # Script mode: use file path
#     PROJECT_ROOT = Path(__file__).resolve().parents[1]
# except NameError:
#     # Notebook mode: use cwd, then go up two parents (like parents[2])
#     PROJECT_ROOT = Path(os.getcwd()).resolve().parents[1]

# DATA_DIR = Path(os.getenv("DATA_DIR", PROJECT_ROOT)).resolve()

# def p(*parts: str) -> Path:
#     """Join under DATA_DIR."""
#     return DATA_DIR.joinpath(*parts)

# def default_workers() -> int:
#     cpu = os.cpu_count() or 2
#     return min(4, max(4, cpu * 2))

# def timeit(label: str, fn: Callable[[], object], logger = None) -> Tuple[object, float]:
#     if logger is None:
#         logger = get_fallback_logger()
#     t0 = time.perf_counter()
#     out = fn()
#     ms = (time.perf_counter() - t0) * 1000.0
#     logger.info("[%s] loaded in %.0f ms", label, ms)
#     return out, ms

# def parallel_read(tasks: Dict[str, Callable[[], object]], max_workers: int | None = None) -> Dict[str, object]:
#     """Run small I/O tasks in parallel; returns dict name -> result."""
#     if max_workers is None:
#         max_workers = default_workers()
#     results: Dict[str, object] = {}
#     errors: list[str] = []
#     with ThreadPoolExecutor(max_workers=max_workers) as ex:
#         fut_map = {ex.submit(fn): name for name, fn in tasks.items()}
#         for fut in as_completed(fut_map):
#             name = fut_map[fut]
#             try:
#                 results[name] = fut.result()
#             except Exception as e:
#                 errors.append(f"{name}: {e!r}")
#     if errors:
#         raise RuntimeError("Parallel read failed:\n  " + "\n  ".join(errors))
#     return results



# def read_parquet_polars(path: str, name: str, logger = None) -> pl.DataFrame:
#     """Reads a Parquet file using Polars, casts all columns to string (Utf8)."""

#     if logger is None:
#         logger = get_fallback_logger()

#     try:
#         df = pl.read_parquet(path)
#         df = df.with_columns([pl.col(col).cast(pl.Utf8) for col in df.columns])
#         # log.info(f"[CTD] Successfully loaded '{name}' from: {path}")
#         return df
#     except Exception as e:
#         logger.error(f"[CTD] Failed to load '{name}' from: {path}\nException: {e}")
#         raise


# def get_fallback_logger(name="biochirp.tmp"):
#     """
#     Return a logger instance for the given name, ensuring logging is always available.

#     If no root logger handlers are set (e.g., the app is run as a standalone script or test),
#     this function will automatically configure a basic console logger with INFO level.
#     This ensures that logs are never lost, whether or not a global logging setup exists.

#     Args:
#         name (str): The name of the logger to retrieve. Use a module- or component-specific
#                     string for easier log filtering. Defaults to "biochirp.tmp".

#     Returns:
#         logging.Logger: Configured logger instance, ready for use.

#     Example:
#         >>> from app.utils.logger import get_fallback_logger
#         >>> logger = get_fallback_logger("biochirp.services")
#         >>> logger.info("Logger is ready!")
#     """

#     import logging
#     logger = logging.getLogger(name)
#     if not logging.getLogger().hasHandlers():
#         logging.basicConfig(
#             level=logging.INFO,
#             format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
#         )
#     return logger


# def ensure_exists(path):
#     """
#     Check if a file exists at the given path.

#     Args:
#         path (str or Path): Path to the file.

#     Returns:
#         str or Path: The same path if the file exists.

#     Raises:
#         FileNotFoundError: If the file does not exist.
#     """
#     if not Path(path).exists():
#         raise FileNotFoundError(f"{path} not found!")
#     return path

# def read_parquet_polars(path, name=None):
#     """
#     Load a Parquet file as a Polars DataFrame.

#     Args:
#         path (str or Path): Path to the Parquet file.
#         name (str, optional): Not used, for API compatibility.

#     Returns:
#         pl.DataFrame: Loaded Polars DataFrame.
#     """
#     return pl.read_parquet(path)



# def return_preprocessed_ctd(max_workers: int | None = None, logger = None) -> dict[str, pl.DataFrame]:
#     # ---- locate files ----
#     f_chem_gene   = ensure_exists(p("data", "chem_gene_association.parquet"))
#     f_chems       = ensure_exists(p("data", "chemical_master_table.parquet"))
#     f_chem_dis    = ensure_exists(p("data", "chemical_disease_association.parquet"))
#     f_diseases    = ensure_exists(p("data", "disease_master_table.parquet"))
#     f_dis_path    = ensure_exists(p("data", "disease_pathway_association.parquet"))
#     f_genes       = ensure_exists(p("data", "gene_master_table.parquet"))
#     f_gene_path   = ensure_exists(p("data", "gene_pathway_association.parquet"))
#     f_pathways    = ensure_exists(p("data", "pathway_master_table.parquet"))




#     if logger is None:
#         logger = get_fallback_logger()


#     logger.info(f_chem_gene)

    

#     logger.info("[CTD] Reading pre-converted Parquet files using Polars (eager mode)")

#     # ---- parallel read ----
#     tasks = {
#         "chemical_gene_association": lambda: read_parquet_polars(f_chem_gene, "chem_gene_association"),
#         "chemical_master_table": lambda: read_parquet_polars(f_chems, "chemical_master_table"),
#         "chemical_disease_association": lambda: read_parquet_polars(f_chem_dis, "chemical_disease_association"),
#         "disease_master_table": lambda: read_parquet_polars(f_diseases, "disease_master_table"),
#         "disease_pathway_association": lambda: read_parquet_polars(f_dis_path, "disease_pathway_association"),
#         "gene_master_table": lambda: read_parquet_polars(f_genes, "gene_master_table"),
#         "gene_pathway_association": lambda: read_parquet_polars(f_gene_path, "gene_pathway_association"),
#         "pathway_master_table": lambda: read_parquet_polars(f_pathways, "pathway_master_table"),
#     }

#     results, _ = timeit("CTD eager read", lambda: parallel_read(tasks, max_workers))

#     # ---- normalize column names ----
#     mapping = {
#         "# ChemicalName": "drug_name", "ChemicalName": "drug_name",
#         "ChemicalID": "drug_id",
#         "GeneSymbol": "gene_name", "# GeneSymbol": "gene_name",
#         "GeneID": "gene_id", "GeneForms": "gene_forms",
#         "DiseaseName": "disease_name", "# DiseaseName": "disease_name",
#         "DiseaseID": "disease_id",
#         "PathwayName": "pathway_name", "# PathwayName": "pathway_name",
#         "PathwayID": "pathway_id",
#         "InferenceGeneSymbol" : "gene_name"
#     }

#     for name, df in results.items():
#         try:
#             df = df.rename({c: mapping[c] for c in df.columns if c in mapping})
#             results[name] = df
#         except Exception as e:
#             logger.warning(f"[CTD] Failed to rename columns in '{name}': {e}")

#     # ---- clean whitespace & drop duplicates ----
#     for key, df in results.items():
#         try:
#             df = df.unique()
#             # df = strip_all_whitespace(df).unique()

#             results[key] = df
#         except Exception as e:
#             logger.warning(f"[CTD] Cleaning failed for '{key}': {e}")

#     # ---- structured return ----
#     return {
#         "chemical_gene_association_ctd": results["chemical_gene_association"],
#         "chemical_master_table_ctd": results["chemical_master_table"],
#         "chemical_disease_association_ctd": results["chemical_disease_association"],
#         "disease_master_table_ctd": results["disease_master_table"],
#         "gene_master_table_ctd": results["gene_master_table"],
#         "gene_pathway_association_ctd": results["gene_pathway_association"],
#         "disease_pathway_association_ctd": results["disease_pathway_association"],
#         "pathway_master_table_ctd": results["pathway_master_table"],
#     }



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



def return_preprocessed_ctd(data_dir="data", logger=None) -> dict[str, pl.DataFrame]:

    import os

    if logger is None:
        logger = get_fallback_logger()

    try:
        logger.info("[CTD] Started loading CTD database...")

        f_chem_gene   = ensure_exists("chem_gene_association.parquet")
        f_chems       = ensure_exists("chemical_master_table.parquet")
        f_chem_dis    = ensure_exists("chemical_disease_association.parquet")
        f_diseases    = ensure_exists("disease_master_table.parquet")
        f_dis_path    = ensure_exists("disease_pathway_association.parquet")
        f_genes       = ensure_exists("gene_master_table.parquet")
        f_gene_path   = ensure_exists("gene_pathway_association.parquet")
        f_pathways    = ensure_exists("pathway_master_table.parquet")

        tasks = {
            "chemical_gene_association": read_parquet_polars(f_chem_gene),
            "chemical_master_table": read_parquet_polars(f_chems),
            "chemical_disease_association": read_parquet_polars(f_chem_dis),
            "disease_master_table": read_parquet_polars(f_diseases),
            "disease_pathway_association": read_parquet_polars(f_dis_path),
            "gene_master_table": read_parquet_polars(f_genes),
            "gene_pathway_association": read_parquet_polars(f_gene_path),
            "pathway_master_table": read_parquet_polars(f_pathways),
        }

        mapping = {
        "# ChemicalName": "drug_name", "ChemicalName": "drug_name",
        "ChemicalID": "drug_id",
        "GeneSymbol": "gene_name", "# GeneSymbol": "gene_name",
        "GeneID": "gene_id", "GeneForms": "gene_forms",
        "DiseaseName": "disease_name", "# DiseaseName": "disease_name",
        "DiseaseID": "disease_id",
        "PathwayName": "pathway_name", "# PathwayName": "pathway_name",
        "PathwayID": "pathway_id",
        "InferenceGeneSymbol" : "gene_name"}

        results = dict()

        for name, df in tasks.items():
            rename_dict = {c: mapping[c] for c in df.columns if c in mapping}
            if rename_dict:
                df = df.rename(rename_dict)
            # df = strip_all_whitespace(df).unique()
            df = df.unique()
            results[name] = df

        logger.info("[CTD] Finished  loading CTD database...")

        return {
        "chemical_gene_association_ctd": results["chemical_gene_association"],
        "chemical_master_table_ctd": results["chemical_master_table"],
        "chemical_disease_association_ctd": results["chemical_disease_association"],
        "disease_master_table_ctd": results["disease_master_table"],
        "gene_master_table_ctd": results["gene_master_table"],
        "gene_pathway_association_ctd": results["gene_pathway_association"],
        "disease_pathway_association_ctd": results["disease_pathway_association"],
        "pathway_master_table_ctd": results["pathway_master_table"],
    }


    except:

        logger.error("[CTD] Error loading CTD database...")