"""
Image Processing Module
GreenMind Project
"""

from PIL import Image
from torchvision import transforms


class ImageProcessor:

    def __init__(self):

        self.transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(
                mean=[0.485, 0.456, 0.406],
                std=[0.229, 0.224, 0.225]
            )
        ])

    def process(self, image):

        if image.mode != "RGB":
            image = image.convert("RGB")

        image_tensor = self.transform(image)

        image_tensor = image_tensor.unsqueeze(0)

        return image_tensor