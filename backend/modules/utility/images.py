import os
from django.core.files.uploadedfile import SimpleUploadedFile


def create_test_image():
    test_image_path = os.path.join(os.path.dirname(__file__), "test_image.jpg")

    with open(test_image_path, "rb") as f:
        test_image = SimpleUploadedFile(
            name="test_image.jpg", content=f.read(), content_type="image/jpeg"
        )
    return test_image
