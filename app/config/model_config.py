
import yaml
from pathlib import Path

def load_model_config(path="app/config/models.yaml"):
    """
    Load a list of biomedical model names from a YAML configuration file.

    The YAML file must contain a top-level key 'biomedical_models' whose value is a list of strings,
    each string representing a model name or model path.

    Args:
        path (str): Path to the YAML configuration file.
                    Default is "config/models.yaml".

    Returns:
        List[str]: A list of biomedical model names.

    Raises:
        FileNotFoundError: If the YAML file does not exist.
        KeyError: If the required 'biomedical_models' key is missing.
        yaml.YAMLError: If the file is not valid YAML.

    Example:
        # config/models.yaml
        # biomedical_models:
        #   - FremyCompany/BioLORD-2023-S
        #   - malteos/scincl

        >>> from config.model_config import load_model_config
        >>> BIOMEDICAL_MODELS = load_model_config()
    """
    with open(Path(path), "r") as f:
        cfg = yaml.safe_load(f)
    return cfg["biomedical_models"]

BIOMEDICAL_MODELS = load_model_config()
