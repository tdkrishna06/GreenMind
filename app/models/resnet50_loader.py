"""
ResNet50 Loader
GreenMind Project
"""

import torch
from torchvision.models import resnet50


class ResNet50Loader:

    def __init__(self):

        print("Loading ResNet50 Model...")

        self.model = resnet50(weights=None)

        self.model.eval()

        print("✅ Model Loaded Successfully!")

    def get_model(self):

        return self.model