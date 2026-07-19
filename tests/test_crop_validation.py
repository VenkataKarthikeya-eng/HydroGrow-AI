import os
import sys
import io
import glob
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from fastapi.testclient import TestClient

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.normpath(os.path.join(BASE_DIR, ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from backend.services.crop_validation_service import crop_validation_service
from backend.api.main import app

client = TestClient(app)

NUTRIENT_CLASSES = ['healthy', 'nitrogen_deficiency', 'phosphorus_deficiency', 'potassium_deficiency']

def find_sample_lettuce_image(class_name):
    cls_dir = os.path.join(PROJECT_ROOT, "data", "nutrient_dataset", class_name)
    imgs = glob.glob(os.path.join(cls_dir, "*.*"))
    if imgs:
        return imgs[0]
    return None

def create_other_plant_leaf_bytes(plant_type='tomato'):
    img = Image.new('RGB', (224, 224), color=(180, 150, 110)) # Soil pot background
    draw = ImageDraw.Draw(img)
    if plant_type == 'tomato':
        # Dark serrated compound leaf shape with non-lettuce olive tint (g < r * 1.05)
        draw.polygon([(112, 30), (70, 80), (50, 120), (90, 140), (112, 190), (134, 140), (174, 120), (154, 80)], fill=(100, 95, 35))
        draw.line([(112, 30), (112, 190)], fill=(120, 110, 45), width=3)
    else: # potato
        draw.ellipse([(40, 30), (184, 194)], fill=(95, 90, 30))
        draw.line([(112, 30), (112, 194)], fill=(115, 105, 40), width=4)
        
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    return buf.getvalue()

def create_document_bytes():
    img = Image.new('RGB', (224, 224), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)
    for y in range(20, 200, 15):
        draw.line([(20, y), (180, y)], fill=(40, 40, 40), width=3)
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    return buf.getvalue()

def create_object_bytes():
    img = Image.new('RGB', (224, 224), color=(220, 220, 220))
    draw = ImageDraw.Draw(img)
    draw.rectangle([(40, 40), (184, 184)], fill=(200, 60, 60))
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    return buf.getvalue()

def create_blurry_low_confidence_bytes():
    # Gray noise image with ambiguous features
    arr = np.random.randint(100, 160, (224, 224, 3), dtype=np.uint8)
    img = Image.fromarray(arr).filter(ImageFilter.BLUR)
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    return buf.getvalue()

def test_crop_validation_direct_inference():
    print("\n--- 1. Testing CropValidationService Direct Inference Across All Cases ---")

    # 1. Healthy Lettuce -> PASS
    healthy_path = find_sample_lettuce_image('healthy')
    with open(healthy_path, 'rb') as f:
        res = crop_validation_service.validate_crop_image(f.read())
    print("1. Healthy Lettuce ->", res)
    assert res["status"] == "allowed"
    assert res["class"] == "lettuce_leaf"
    assert res["confidence"] >= 0.90

    # 2. Nitrogen Deficiency Lettuce -> PASS
    n_path = find_sample_lettuce_image('nitrogen_deficiency')
    with open(n_path, 'rb') as f:
        res = crop_validation_service.validate_crop_image(f.read())
    print("2. Nitrogen Lettuce ->", res)
    assert res["status"] == "allowed"

    # 3. Phosphorus Deficiency Lettuce -> PASS
    p_path = find_sample_lettuce_image('phosphorus_deficiency')
    with open(p_path, 'rb') as f:
        res = crop_validation_service.validate_crop_image(f.read())
    print("3. Phosphorus Lettuce ->", res)
    assert res["status"] == "allowed"

    # 4. Potassium Deficiency Lettuce -> PASS
    k_path = find_sample_lettuce_image('potassium_deficiency')
    with open(k_path, 'rb') as f:
        res = crop_validation_service.validate_crop_image(f.read())
    print("4. Potassium Lettuce ->", res)
    assert res["status"] == "allowed"

    # 5. Tomato Leaf -> REJECT (other_plant_leaf)
    tomato_bytes = create_other_plant_leaf_bytes('tomato')
    res = crop_validation_service.validate_crop_image(tomato_bytes)
    print("5. Tomato Leaf ->", res)
    assert res["status"] == "rejected"
    assert res["class"] == "other_plant_leaf"
    assert "another plant" in res["reason"]

    # 6. Potato Leaf -> REJECT (other_plant_leaf)
    potato_bytes = create_other_plant_leaf_bytes('potato')
    res = crop_validation_service.validate_crop_image(potato_bytes)
    print("6. Potato Leaf ->", res)
    assert res["status"] == "rejected"
    assert res["class"] == "other_plant_leaf"

    # 7. Document Image -> REJECT (non_leaf)
    doc_bytes = create_document_bytes()
    res = crop_validation_service.validate_crop_image(doc_bytes)
    print("7. Document Image ->", res)
    assert res["status"] == "rejected"
    assert res["class"] == "non_leaf"
    assert "Invalid image" in res["reason"]

    # 8. Random Object -> REJECT (non_leaf)
    obj_bytes = create_object_bytes()
    res = crop_validation_service.validate_crop_image(obj_bytes)
    print("8. Random Object ->", res)
    assert res["status"] == "rejected"
    assert res["class"] == "non_leaf"

    # 9. Blurry/Low-Confidence Image -> REJECT
    blur_bytes = create_blurry_low_confidence_bytes()
    res = crop_validation_service.validate_crop_image(blur_bytes)
    print("9. Blurry Low-Confidence Image ->", res)
    assert res["status"] == "rejected"

def test_api_crop_validation_gatekeeper():
    print("\n--- 2. Testing FastAPI /api/vision/plant-analysis Gatekeeper ---")

    # 2.1 Valid Lettuce Image passes and returns Model 1 & Model 2 predictions
    healthy_path = find_sample_lettuce_image('healthy')
    with open(healthy_path, 'rb') as f:
        res = client.post("/api/vision/plant-analysis", files={"file": ("lettuce.png", f, "image/png")})
    assert res.status_code == 200
    data = res.json()
    print("2.1 Valid Lettuce API Response:", data)
    assert "growth_prediction" in data
    assert "nutrient_prediction" in data

    # 2.2 Tomato Leaf Image rejected by API
    tomato_bytes = create_other_plant_leaf_bytes('tomato')
    res = client.post("/api/vision/plant-analysis", files={"file": ("tomato.png", tomato_bytes, "image/png")})
    assert res.status_code == 400
    data = res.json()
    print("2.2 Tomato Leaf API Rejection Response:", data)
    assert data["status"] == "rejected"
    assert data["class"] == "other_plant_leaf"

    # 2.3 Document Image rejected by API
    doc_bytes = create_document_bytes()
    res = client.post("/api/vision/plant-analysis", files={"file": ("doc.png", doc_bytes, "image/png")})
    assert res.status_code == 400
    data = res.json()
    print("2.3 Document API Rejection Response:", data)
    assert data["status"] == "rejected"
    assert data["class"] == "non_leaf"

if __name__ == '__main__':
    test_crop_validation_direct_inference()
    test_api_crop_validation_gatekeeper()
    print("\nALL PRODUCTION CROP VALIDATOR TESTS PASSED SUCCESSFULLY!")
