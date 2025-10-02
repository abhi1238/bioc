
import polars as pl
from pathlib import Path
import logging
from os import getcwd
import os
from polars import col, String 
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Callable, Dict, Iterable, Tuple

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


def default_workers() -> int:
    cpu = os.cpu_count() or 2
    return min(4, max(4, cpu * 2))

def timeit(label: str, fn: Callable[[], object], logger = None) -> Tuple[object, float]:
    if logger is None:
        logger = get_fallback_logger()
    t0 = time.perf_counter()
    out = fn()
    ms = (time.perf_counter() - t0) * 1000.0
    logger.info("[%s] loaded in %.0f ms", label, ms)
    return out, ms

def parallel_read(tasks: Dict[str, Callable[[], object]], max_workers: int | None = None) -> Dict[str, object]:
    """Run small I/O tasks in parallel; returns dict name -> result."""
    if max_workers is None:
        max_workers = default_workers()
    results: Dict[str, object] = {}
    errors: list[str] = []
    with ThreadPoolExecutor(max_workers=max_workers) as ex:
        fut_map = {ex.submit(fn): name for name, fn in tasks.items()}
        for fut in as_completed(fut_map):
            name = fut_map[fut]
            try:
                results[name] = fut.result()
            except Exception as e:
                errors.append(f"{name}: {e!r}")
    if errors:
        raise RuntimeError("Parallel read failed:\n  " + "\n  ".join(errors))
    return results



def return_preprocessed_hcdt(max_workers: int | None = None, logger = None) -> dict[str, pl.DataFrame]:


    import os

    if logger is None:
        logger = get_fallback_logger()

    # ---- file paths (all Parquet now) ----
    f_drug       = ensure_exists("drug_master_table.parquet")
    f_drug_gene  = ensure_exists("drug_gene_association.parquet")
    f_drug_dis   = ensure_exists("drug_disease_association.parquet")
    f_drug_path  = ensure_exists("drug_pathway_association.parquet")
    f_path_gene  = ensure_exists("pathway_gene_association.parquet")
    # f_rna_target = ensure_exists(p("hcdt", "RNA-TargetGene.parquet"))
    f_disease = ensure_exists("disease_master_table.parquet")
    f_gene = ensure_exists("gene_master_table.parquet")
    f_path = ensure_exists("pathway_master_table.parquet")

    logger.info("[HCDT] Reading all Parquet files with Polars")

    # ---- file reading tasks ----
    tasks = {
        "drug_master_table":          read_parquet_polars(f_drug),
        "drug_gene_association":      read_parquet_polars(f_drug_gene),
        "drug_disease_association":   read_parquet_polars(f_drug_dis),
        "drug_pathway_association":   read_parquet_polars(f_drug_path),
        "pathway_gene_association":   read_parquet_polars(f_path_gene),
        "disease_master_table":  read_parquet_polars(f_disease),
        "gene_master_table": read_parquet_polars(f_disease),
        "pathway_master_table": read_parquet_polars(f_path),
        # "rna_targetgene_association": lambda: read_parquet_polars(f_rna_target, "rna_targetgene_association"),
    }

    # results, _ = timeit("HCDT Parquet read (Polars)", parallel_read(tasks, max_workers))

    # ---- column renaming ----
    mapping = {
        "DRUG_NAME": "drug_name", "Drug_Name": "drug_name",
        "GENE_SYMBOL": "gene_name", "Target": "gene_name",
        "# Disease_Name": "disease_name", "Disease_Name": "disease_name",
        "PathwayID": "pathway_id", "PATH_NAME": "pathway_name", "path_name": "pathway_name",
        "Pubchem_CID": "PUBCHEM_CID"
    }

    results = dict()

    for name, df in tasks.items():
        rename_dict = {c: mapping[c] for c in df.columns if c in mapping}
        if rename_dict:
            df = df.rename(rename_dict)


        # df = strip_all_whitespace(df).unique()
        df = df.unique()
        results[name] = df

    logger.info("[HCDT] Finished  loading HCDT database...")

    # ---- return final output ----
    return {
        "drug_master_table_hcdt": results["drug_master_table"],
        "drug_gene_association_hcdt": results["drug_gene_association"],
        "drug_disease_association_hcdt": results["drug_disease_association"],
        "drug_pathway_association_hcdt": results["drug_pathway_association"],
        "pathway_gene_association_hcdt": results["pathway_gene_association"],
        # "rna_targetgene_association_hcdt": results["rna_targetgene_association"],
        "disease_master_table_hcdt": results["disease_master_table"],
        "gene_master_table_hcdt": results["gene_master_table"],
        "pathway_master_table_hcdt": results["pathway_master_table"],
        # "disease_master_table": results["disease_master_table"],

    }