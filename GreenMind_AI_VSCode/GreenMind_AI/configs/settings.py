"""Application paths and inference configuration."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODEL_ID = "mesabo/agri-plant-disease-resnet50"
MODEL_CACHE = ROOT / "model_cache"
DATA_DIR = ROOT / "data"
HISTORY_FILE = DATA_DIR / "history.json"
MAX_UPLOAD_BYTES = 10 * 1024 * 1024
