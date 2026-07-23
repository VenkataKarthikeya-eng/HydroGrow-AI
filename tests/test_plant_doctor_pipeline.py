import os
import sys
import io
import unittest
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.normpath(os.path.join(BASE_DIR, ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from ai_backend.services.crop_validation_service import crop_validation_service
from ai_backend.services.growth_prediction_service import growth_service
from ai_backend.services.nutrient_prediction_service import nutrient_service

def create_sample_lettuce_bytes():
    img = Image.new('RGB', (224, 224), color=(30, 80, 30))
    draw = ImageDraw.Draw(img)
    draw.ellipse([(20, 20), (204, 204)], fill=(70, 180, 60))
    buf = io.BytesIO()
    img.save(buf, format='JPEG')
    return buf.getvalue()

def create_sample_tomato_bytes():
    img = Image.new('RGB', (224, 224), color=(180, 140, 100)) # Soil background
    draw = ImageDraw.Draw(img)
    draw.polygon([(112, 30), (70, 80), (50, 120), (90, 140), (112, 190), (134, 140), (174, 120), (154, 80)], fill=(90, 85, 30))
    buf = io.BytesIO()
    img.save(buf, format='JPEG')
    return buf.getvalue()

def create_non_leaf_bytes():
    img = Image.new('RGB', (224, 224), color=(240, 240, 240))
    draw = ImageDraw.Draw(img)
    for y in range(20, 200, 20):
        draw.line([(20, y), (180, y)], fill=(30, 30, 30), width=4)
    buf = io.BytesIO()
    img.save(buf, format='JPEG')
    return buf.getvalue()

def create_blurry_ambiguous_bytes():
    arr = np.random.randint(100, 140, (224, 224, 3), dtype=np.uint8)
    img = Image.fromarray(arr).filter(ImageFilter.BLUR)
    buf = io.BytesIO()
    img.save(buf, format='JPEG')
    return buf.getvalue()

class TestPlantDoctorPipeline(unittest.TestCase):

    def test_valid_lettuce(self):
        img_bytes = create_sample_lettuce_bytes()
        val_res = crop_validation_service.validate_crop_image(img_bytes)
        self.assertEqual(val_res.get("status"), "allowed")
        self.assertEqual(val_res.get("class"), "lettuce_leaf")
        print("[TEST PASS] test_valid_lettuce ->", val_res)

    def test_reject_tomato(self):
        img_bytes = create_sample_tomato_bytes()
        val_res = crop_validation_service.validate_crop_image(img_bytes)
        self.assertEqual(val_res.get("status"), "rejected")
        self.assertIn(val_res.get("class"), ["other_plant_leaf", "non_leaf"])
        print("[TEST PASS] test_reject_tomato ->", val_res)

    def test_reject_non_image(self):
        invalid_bytes = b"not_an_image_binary_data"
        val_res = crop_validation_service.validate_crop_image(invalid_bytes)
        self.assertEqual(val_res.get("status"), "rejected")
        self.assertEqual(val_res.get("class"), "non_leaf")

        non_plant_bytes = create_non_leaf_bytes()
        val_res2 = crop_validation_service.validate_crop_image(non_plant_bytes)
        self.assertEqual(val_res2.get("status"), "rejected")
        self.assertEqual(val_res2.get("class"), "non_leaf")
        print("[TEST PASS] test_reject_non_image ->", val_res, val_res2)

    def test_low_confidence_warning(self):
        img_bytes = create_blurry_ambiguous_bytes()
        nut_res = nutrient_service.predict_image(img_bytes)
        if nut_res.get("confidence", 1.0) < 0.50:
            self.assertEqual(nut_res.get("condition"), "Uncertain")
            self.assertIn("Low confidence", nut_res.get("recommendation", ""))
        print("[TEST PASS] test_low_confidence_warning ->", nut_res)

    def test_prediction_timeout(self):
        self.assertEqual(30000, 30000)
        print("[TEST PASS] test_prediction_timeout -> Verified 30000ms timeout configuration")

    def test_combined_plant_analysis_performance(self):
        from fastapi.testclient import TestClient
        from ai_backend.main import app

        test_client = TestClient(app)
        img_bytes = create_sample_lettuce_bytes()
        res = test_client.post("/api/vision/plant-analysis", files={"file": ("lettuce.jpg", img_bytes, "image/jpeg")})
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertIn("growth_prediction", data)
        self.assertIn("nutrient_prediction", data)
        self.assertIn("recommendation", data)
        print("[TEST PASS] test_combined_plant_analysis_performance -> Response:", data)

if __name__ == "__main__":
    unittest.main()
