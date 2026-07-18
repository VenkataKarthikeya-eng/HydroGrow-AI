import unittest
from io import BytesIO
from fastapi import UploadFile
from backend.services.vision.image_processor import ImageProcessor

class TestImageProcessing(unittest.TestCase):
    def test_validate_valid_image(self):
        file = UploadFile(filename="lettuce.png", file=BytesIO(b"dummy image content"))
        self.assertTrue(ImageProcessor.validate_image(file))
        
        file_jpg = UploadFile(filename="crop.jpg", file=BytesIO(b"dummy image"))
        self.assertTrue(ImageProcessor.validate_image(file_jpg))

    def test_validate_invalid_extension(self):
        file = UploadFile(filename="malicious.sh", file=BytesIO(b"echo hello"))
        self.assertFalse(ImageProcessor.validate_image(file))

    def test_validate_size_exceeded(self):
        large_bytes = b"0" * (6 * 1024 * 1024)
        file = UploadFile(filename="huge.png", file=BytesIO(large_bytes))
        self.assertFalse(ImageProcessor.validate_image(file))
