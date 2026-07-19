import os
import sys

try:
    import pytest
except ImportError:
    pytest = None
from fastapi.testclient import TestClient

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.normpath(os.path.join(BASE_DIR, ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from backend.services.growth_prediction_service import growth_service
from backend.api.main import app

client = TestClient(app)

def test_growth_prediction_service_direct():
    # Find a real image sample from dataset
    sample_img_path = None
    dataset_dir = os.path.join(PROJECT_ROOT, "data", "growth_dataset")
    
    for root, dirs, files in os.walk(dataset_dir):
        for f in files:
            if f.endswith('.png'):
                sample_img_path = os.path.join(root, f)
                break
        if sample_img_path:
            break
            
    assert sample_img_path is not None, "No test image found in dataset!"
    
    with open(sample_img_path, 'rb') as f:
        img_bytes = f.read()
        
    result = growth_service.predict_image(img_bytes)
    
    print("\nInference Output Test Result:")
    print(result)
    
    assert "growth_stage" in result
    assert result["growth_stage"] in ['Seedling', 'Vegetative', 'Mature / Harvest']
    assert "growth_day" in result
    assert 1 <= result["growth_day"] <= 30
    assert "confidence" in result
    assert 0.0 <= result["confidence"] <= 1.0
    assert "recommendation" in result
    assert len(result["recommendation"]) > 0

def test_fastapi_predict_growth_endpoint():
    # Find a real image sample from dataset
    sample_img_path = None
    dataset_dir = os.path.join(PROJECT_ROOT, "data", "growth_dataset")
    
    for root, dirs, files in os.walk(dataset_dir):
        for f in files:
            if f.endswith('.png'):
                sample_img_path = os.path.join(root, f)
                break
        if sample_img_path:
            break

    with open(sample_img_path, 'rb') as f:
        response = client.post(
            "/api/vision/predict-growth",
            files={"file": ("test_plant.png", f, "image/png")}
        )
        
    assert response.status_code == 200, f"API failed with {response.status_code}: {response.text}"
    data = response.json()
    
    print("\nFastAPI Endpoint Response:")
    print(data)
    
    assert "growth_stage" in data
    assert "growth_day" in data
    assert "confidence" in data
    assert "recommendation" in data

if __name__ == '__main__':
    test_growth_prediction_service_direct()
    test_fastapi_predict_growth_endpoint()
    print("\nALL TESTS PASSED SUCCESSFULLY!")
