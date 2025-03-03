import os

from django.core.exceptions import ValidationError
from PIL import Image


def validate_icon_image_size(image):
    if image:
        with Image.open(image) as img:
            if img.width > 70 or img.height > 70:
                raise ValidationError(
                    f"Icon image must be 70x70 pixels or smaller. Size you provided: {img.size}"  # noqa
                )


def validate_image_file_extension(image):
    ext = os.path.split(image.name)[1]
    valid_extensions = [".png", ".jpg", ".jpeg", ".svg", ".ico"]
    if ext.lower() not in valid_extensions:
        raise ValidationError(
            f"Unsupported file extension: {ext}. Supported extensions: {', '.join(valid_extensions)}"  # noqa
        )
