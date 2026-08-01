from transformers import AutoImageProcessor, AutoModelForImageClassification

MODEL_NAME = "mesabo/agri-plant-disease-resnet50"

processor = AutoImageProcessor.from_pretrained(MODEL_NAME)
model = AutoModelForImageClassification.from_pretrained(MODEL_NAME)

def load_model():
    return processor, model