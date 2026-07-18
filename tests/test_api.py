import sys
import os
import unittest
from fastapi.testclient import TestClient

# Add project root to path for imports
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.normpath(os.path.join(BASE_DIR, "..")))

from backend.api.main import app

class TestHydroGrowAPI(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)
        self.sample_inputs = {
            "air_temperature": 22.0,
            "humidity": 60.0,
            "co2": 450.0,
            "water_ph": 6.2,
            "water_ec": 2.0,
            "water_temperature": 23.0,
            "nutrient_solution": 400.0,
            "water_consumption": 170.0,
            "seedling_height": 12.0,
            "seedling_weight": 4.0,
            "root_length": 7.0,
        }

    def test_health_endpoint(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn(data["status"], ["running", "healthy"])
        self.assertEqual(data["service"], "HydroGrow AI API")

    def test_prediction_endpoint(self):
        response = self.client.post("/api/predict", json=self.sample_inputs)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        # Check that prediction section exists
        self.assertIn("prediction", data)
        self.assertIn("predicted_weight", data["prediction"])
        self.assertIn("growth_category", data["prediction"])
        
        # Check that validation section exists
        self.assertIn("validation", data)
        self.assertIn("prediction_value", data["validation"])
        self.assertIn("original_prediction", data["validation"])
        self.assertIn("was_adjusted", data["validation"])
        self.assertIn("validation_message", data["validation"])
        
        # Check that recommendations and explanation exist
        self.assertIn("recommendations", data)
        self.assertIsInstance(data["recommendations"], list)
        self.assertIn("explanation", data)
        self.assertIn("summary", data["explanation"])
        self.assertIn("positive_factors", data["explanation"])
        self.assertIn("improvement_opportunities", data["explanation"])
        
        # Check that metadata exists
        self.assertIn("metadata", data)
        self.assertIn("derived_inputs", data["metadata"])
        self.assertEqual(data["metadata"]["derived_inputs"]["water_tds"], 1.0)
        self.assertEqual(data["metadata"]["derived_inputs"]["acid_consumption_ml"], 40.0)

    def test_prediction_validation_error(self):
        # Missing field (e.g., air_temperature)
        incomplete_inputs = self.sample_inputs.copy()
        del incomplete_inputs["air_temperature"]
        response = self.client.post("/api/predict", json=incomplete_inputs)
        self.assertEqual(response.status_code, 422)
        data = response.json()
        self.assertTrue(data["error"])
        self.assertIn("Validation failed", data["message"])
        self.assertIn("details", data)

    def test_chat_endpoint_basic(self):
        payload = {
            "message": "Why is my prediction only 245g?",
            "conversation_history": [],
            "context": {
                "user_inputs": {
                    "water_ph": 4.5,
                    "water_ec": 2.0,
                    "water_tds": 1.0,
                    "water_temperature": 21.0,
                    "air_temperature": 22.0,
                    "humidity": 60.0,
                    "co2": 350.0,
                    "nutrient_solution_ml": 400.0,
                    "water_consumption_l": 170.0,
                    "acid_consumption_ml": 40.0,
                    "initial_height_cm": 12.0,
                    "initial_weight_g": 4.0,
                    "initial_root_length_cm": 7.0,
                },
                "prediction_result": {
                    "prediction_value": 245.5,
                    "growth_category": "Poor"
                },
                "recommendation_outputs": [],
                "explanation_output": {
                    "improvement_opportunities": [
                        {"factor": "Water pH", "explanation": "Water pH is critically low."}
                    ]
                }
            }
        }
        response = self.client.post("/api/chat", json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("response", data)
        self.assertIn("intent", data)
        self.assertIn("sources", data)
        self.assertEqual(data["intent"], "prediction_diagnostic")

    def test_chat_endpoint_fallback(self):
        payload = {
            "message": "some unrecognized topic placeholder query",
            "conversation_history": [],
            "context": {}
        }
        response = self.client.post("/api/chat", json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("response", data)
        self.assertEqual(data["intent"], "fallback")

if __name__ == "__main__":
    unittest.main()
