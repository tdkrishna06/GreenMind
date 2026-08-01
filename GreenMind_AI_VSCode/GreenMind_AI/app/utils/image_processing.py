"""Safe image validation and normalization."""
from __future__ import annotations
from io import BytesIO
from PIL import Image, UnidentifiedImageError


def load_upload(raw: bytes) -> Image.Image:
    """Validate raw upload bytes and return an RGB image."""
    try:
        image = Image.open(BytesIO(raw))
        image.verify()
        image = Image.open(BytesIO(raw)).convert("RGB")
    except (UnidentifiedImageError, OSError, ValueError) as exc:
        raise ValueError("This file is not a valid JPG or PNG image.") from exc
    if image.width < 32 or image.height < 32:
        raise ValueError("Please upload an image at least 32 × 32 pixels.")
    return image
