import os
import sys
import io
import glob
from PIL import Image, ImageDraw
from fastapi.testclient import TestClient

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.normpath(os.path.join(BASE_DIR, ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from backend.services.leaf_validation_service import leaf_validation_service
from backend.api.main import app

client = TestClient(app)

NUTRIENT_CLASSES = ['healthy', 'nitrogen_deficiency', 'phosphorus_deficiency', 'potassium_deficiency']

def find_sample_image(class_name):
    cls_dir = os.path.join(PROJECT_ROOT, "data", "nutrient_dataset", class_name)
    imgs = glob.glob(os.path.join(cls_dir, "*.*"))
    if imgs:
        return imgs[0]
    return None

def create_document_image_bytes():
    img = Image.new('RGB', (224, 224), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)
    for y in range(20, 200, 15):
        draw.line([(20, y), (180, y)], fill=(30, 30, 30), width=3)
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    return buf.getvalue()

def create_random_object_image_bytes():
    img = Image.new('RGB', (224, 224), color=(200, 50, 50))
    draw = ImageDraw.Draw(img)
    draw.rectangle([(50, 50), (170, 170)], fill=(50, 50, 200))
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    return buf.getvalue()

def test_leaf_validation_service_direct():
    print("\n--- 1. Testing LeafValidationService Direct Inference ---")
    
    # 1.1 Test real lettuce leaf samples
    for cls in NUTRIENT_CLASSES:
        img_path = find_sample_image(cls)
        assert img_path is not None, f"No sample image for '{cls}'"
        with open(img_path, 'rb') as f:
            bytes_data = f.read()
        res = leaf_validation_service.validate_image(bytes_data)
        print(f"Leaf sample '{cls}' -> Result: {res}")
        assert "is_leaf" in res
        assert "confidence" in res
        assert res["is_leaf"] is True

    # 1.2 Test document image
    doc_bytes = create_document_image_bytes()
    doc_res = leaf_validation_service.validate_image(doc_bytes)
    print(f"Document image -> Result: {doc_res}")
    assert doc_res["is_leaf"] is False

    # 1.3 Test random non-leaf object image
    obj_bytes = create_random_object_image_bytes()
    obj_res = leaf_validation_service.validate_image(obj_bytes)
    print(f"Random object image -> Result: {obj_res}")
    assert obj_res["is_leaf"] is False

def test_api_leaf_validation_guard():
    print("\n--- 2. Testing FastAPI /api/vision/plant-analysis Leaf Guard ---")

    # 2.1 Valid Lettuce Image should pass and return combined analysis
    leaf_path = find_sample_image('healthy')
    with open(leaf_path, 'rb') as f:
        res = client.post("/api/vision/plant-analysis", files={"file": ("leaf.png", f, "image/png")})
    assert res.status_code == 200
    data = res.json()
    print("Valid Leaf API Response:", data)
    assert "growth_prediction" in data
    assert "nutrient_prediction" in data

    # 2.2 Document Image should be rejected early by Model 3 Guard
    doc_bytes = create_document_image_bytes()
    res = client.post("/api/vision/plant-analysis", files={"file": ("document.png", doc_bytes, "image/png")})
    assert res.status_code == 400
    err_data = res.json()
    print("Document Rejection API Response:", err_data)
    assert "error" in err_data
    assert "Invalid image" in err_data["error"]
    assert err_data.get("is_leaf") is False

    # 2.3 Random Object Image should be rejected early
    obj_bytes = create_random_object_image_bytes()
    res = client.post("/api/vision/plant-analysis", files={"file": ("object.png", obj_bytes, "image/png")})
    assert res.status_code == 400
    err_data = res.json()
    print("Random Object Rejection API Response:", err_data)
    assert "error" in err_data
    assert "Invalid image" in err_data["error"]

if __name__ == '__main__':
    test_leaf_validation_service_direct()
    test_api_leaf_validation_guard()
    print("\nALL MODEL 3 LEAF VALIDATOR TESTS PASSED SUCCESSFULLY!")
