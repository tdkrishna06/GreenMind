from PIL import Image

from app.models.model_loader import PlantDiseaseModel


model = PlantDiseaseModel()


image = Image.open("datasets/test.jpg").convert("RGB")


disease, confidence = model.predict(image)


print()

print("Prediction :", disease)

print("Confidence :", confidence)