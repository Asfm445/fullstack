import os

from django.core.exceptions import ValidationError
from PIL import Image


def validate_icon_image_size(image):
    if image:
        with Image.open(image) as img:
            if img.width > 70 or img.height > 70:
                raise ValidationError(
                    f"the maximum allowed dimentions for the image are 70x70 the image you uploaded is {img.width}x{img.height}"
                )


def validate_image_file_extention(value):
    ext = os.path.splitext(value.name)[1]
    valid_extentions = [".jpg", ".jpeg", ".png", "gif"]
    if ext.lower() not in valid_extentions:
        raise ValidationError("unsupported file extentions")
