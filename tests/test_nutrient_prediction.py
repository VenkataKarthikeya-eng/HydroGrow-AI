import os
import sys
import glob
from fastapi.testclient import TestClient

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.normpath(os.path.join(BASE_DIR, ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from backend.services.nutrient_prediction_service import nutrient_service
from backend.api.main import app

client = TestClient(app)

CLASSES = ['healthy', 'nitrogen_deficiency', 'phosphorus_deficiency', 'potassium_deficiency']

def find_sample_image(class_name):
    cls_dir = os.path.join(PROJECT_ROOT, "data", "nutrient_dataset", class_name)
    imgs = glob.glob(os.path.join(cls_dir, "*.*"))
    if imgs:
        return imgs[0]
    return None

def test_direct_nutrient_inference_all_classes():
    print("\n--- Testing Direct NutrientPredictionService Inference Across Classes ---")
    for cls in CLASSES:
        img_path = find_sample_image(cls)
        assert img_path is not None, f"Sample image for class '{cls}' not found!"
        
        with open(img_path, 'rb') as f:
            img_bytes = f.read()
            
        result = nutrient_service.predict_image(img_bytes)
        print(f"Class '{cls}' -> Predicted: {result}")
        
        assert "condition" in result
        assert "confidence" in result
        assert "recommendation" in result
        assert 0.0 <= result["confidence"] <= 1.0
        assert len(result["recommendation"]) > 0

def test_fastapi_predict_nutrient_endpoint():
    print("\n--- Testing FastAPI /api/vision/predict-nutrient Endpoint ---")
    img_path = find_sample_image('nitrogen_deficiency')
    assert img_path is not None
    
    with open(img_path, 'rb') as f:
        response = client.post(
            "/api/vision/predict-nutrient",
            files={"file": ("leaf_test.png", f, "image/png")}
        )
        
    assert response.status_code == 200, f"API failed with {response.status_code}: {response.text}"
    data = response.json()
    print("Response JSON:", data)
    assert "condition" in data
    assert "confidence" in data
    assert "recommendation" in data

def test_fastapi_plant_analysis_combined_endpoint():
    print("\n--- Testing FastAPI /api/vision/plant-analysis Combined Endpoint ---")
    img_path = find_sample_image('healthy')
    assert img_path is not None
    
    with open(img_path, 'rb') as f:
        response = client.post(
            "/api/vision/plant-analysis",
            files={"file": ("plant_test.png", f, "image/png")}
        )
        
    assert response.status_code == 200, f"API failed with {response.status_code}: {response.text}"
    data = response.json()
    print("Combined Scanner Response JSON:", data)
    assert "growth_prediction" in data
    assert "nutrient_prediction" in data
    assert "recommendation" in data
    assert "stage" in data["growth_prediction"]
    assert "growth_day" in data["growth_prediction"]
    assert "condition" in data["nutrient_prediction"]

if __name__ == '__main__':
    test_direct_nutrient_inference_all_classes()
    test_fastapi_predict_nutrient_endpoint()
    test_fastapi_plant_analysis_combined_endpoint()
    print("\nALL NUTRIENT AI TESTS PASSED SUCCESSFULLY!")
