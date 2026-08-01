from app.models.resnet50_loader import ResNet50Loader

print("Creating Loader...")

loader = ResNet50Loader()

print("Getting Model...")

model = loader.get_model()

print("Model Loaded Successfully!")

print(model)