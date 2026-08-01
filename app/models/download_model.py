from transformers import AutoImageProcessor
from transformers import AutoModelForImageClassification

MODEL_NAME = "mesabo/agri-plant-disease-resnet50"
MODEL_CACHE = "model_weights"

print("Downloading image processor...")

processor = AutoImageProcessor.from_pretrained(
    MODEL_NAME,
    cache_dir=MODEL_CACHE
)

print("Downloading AI model...")

model = AutoModelForImageClassification.from_pretrained(
    MODEL_NAME,
    cache_dir=MODEL_CACHE
)

print("✅ Download completed successfully!")