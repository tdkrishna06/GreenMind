from app.diagnosis.predict import DiseasePredictor
from app.labels.class_names import CLASS_NAMES
from app.database.remedy_loader import get_remedy

predictor = DiseasePredictor()

prediction, confidence = predictor.predict("datasets/test.jpg")

disease_name = CLASS_NAMES.get(prediction, "Unknown Disease")

print("=" * 60)
print("Disease    :", disease_name)
print("Confidence :", round(confidence * 100, 2), "%")

remedy = get_remedy(disease_name)

if remedy:
    print("\nSymptoms:")
    for item in remedy["symptoms"]:
        print("-", item)

    print("\nTraditional Remedy:")
    for item in remedy["traditional_remedy"]:
        print("-", item)

    print("\nPrevention:")
    for item in remedy["prevention"]:
        print("-", item)
else:
    print("\nNo remedy found for this disease.")

print("=" * 60)