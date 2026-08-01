from PIL import Image
import torch

from app.models.model_loader import load_model


class DiseasePredictor:

    def __init__(self):
        self.processor, self.model = load_model()

    def predict(self, image_path):

        image = Image.open(image_path).convert("RGB")

        inputs = self.processor(images=image, return_tensors="pt")

        with torch.no_grad():
            outputs = self.model(**inputs)

        logits = outputs.logits

        predicted_class = logits.argmax(-1).item()

        confidence = torch.softmax(logits, dim=-1)[0][predicted_class].item()

        return predicted_class, confidence