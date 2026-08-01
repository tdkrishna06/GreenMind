"""Model inference service."""
from __future__ import annotations
from dataclasses import dataclass
from time import perf_counter
from PIL import Image
import torch
from app.models.model_loader import load_model


@dataclass(frozen=True)
class Prediction:
    """One diagnosis outcome."""
    label: str
    confidence: float
    inference_seconds: float
    top_predictions: list[tuple[str, float]]


class DiseasePredictor:
    """Runs a cached ResNet50 plant disease classifier."""

    def predict(self, image: Image.Image) -> Prediction:
        processor, model = load_model()
        started = perf_counter()
        inputs = processor(images=image, return_tensors="pt")
        with torch.inference_mode():
            probabilities = torch.softmax(model(**inputs).logits[0], dim=-1)
        scores, indices = torch.topk(probabilities, k=min(3, probabilities.numel()))
        labels = model.config.id2label
        top = [(labels[int(index)], float(score)) for score, index in zip(scores, indices)]
        return Prediction(top[0][0], top[0][1], perf_counter() - started, top)
