from pathlib import Path

# High-level Directories
CONFIG_DIR = Path(__file__).resolve()
APP_DIR = CONFIG_DIR.parent.parent

TITANIC_DATASET = APP_DIR.parent / "titanic_dataset" / "train.csv"
