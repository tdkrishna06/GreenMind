"""Lazy Hugging Face model loader."""
from __future__ import annotations
import logging
from functools import lru_cache
from transformers import AutoImageProcessor, AutoModelForImageClassification
from configs.settings import MODEL_CACHE, MODEL_ID

LOGGER = logging.getLogger(__name__)


@lru_cache(maxsize=1)
def load_model():
    """Download (on first launch) and cache the classifier locally."""
    try:
        MODEL_CACHE.mkdir(parents=True, exist_ok=True)
        processor = AutoImageProcessor.from_pretrained(MODEL_ID, cache_dir=str(MODEL_CACHE))
        model = AutoModelForImageClassification.from_pretrained(MODEL_ID, cache_dir=str(MODEL_CACHE))
        model.eval()
        return processor, model
    except Exception as exc:
        LOGGER.exception("Unable to load plant disease model")
        raise RuntimeError(
            "The AI model could not be loaded. On the first launch, connect to the internet "
            "so GreenMind AI can download the public model (about 100 MB)."
        ) from exc
