"""
test_prediction_validation.py — Unit Tests for Prediction Validation Layer

This test script validates the behavior of the prediction validation layer using:
1. Direct module level function tests for boundary conditions, normal values, and extreme values.
2. Prediction pipeline integration tests with realistic and extreme inputs.
"""

import sys
import os
import unittest

# Try to reconfigure stdout to UTF-8 to prevent UnicodeEncodeErrors with emojis on Windows
try:
    sys.stdout.reconfigure(encoding='utf-8')
except AttributeError:
    pass

# Ensure the project root folder is in the python path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.normpath(os.path.join(BASE_DIR, "..")))

from backend.services.prediction.prediction_validation import (
    validate_prediction,
    MIN_WEIGHT,
    MAX_WEIGHT,
    MEAN_WEIGHT,
    P5_WEIGHT,
    P95_WEIGHT
)
from backend.services.prediction.prediction import predict


class TestPredictionValidationLayer(unittest.TestCase):
    
    def test_target_distribution_constants(self):
        """Verify that training distribution constants are successfully loaded and realistic."""
        self.assertIsNotNone(MIN_WEIGHT)
        self.assertIsNotNone(MAX_WEIGHT)
        self.assertIsNotNone(MEAN_WEIGHT)
        self.assertIsNotNone(P5_WEIGHT)
        self.assertIsNotNone(P95_WEIGHT)
        
        # Verify logical relationships
        self.assertTrue(MIN_WEIGHT < P5_WEIGHT < MEAN_WEIGHT < P95_WEIGHT < MAX_WEIGHT)
        print(f"\n[INFO] Training Dataset Stats Loaded:")
        print(f"  - Minimum weight: {MIN_WEIGHT} g")
        print(f"  - 5th Percentile (Lower Bound): {P5_WEIGHT} g")
        print(f"  - Mean weight: {MEAN_WEIGHT:.2f} g")
        print(f"  - 95th Percentile (Upper Bound): {P95_WEIGHT} g")
        print(f"  - Maximum weight: {MAX_WEIGHT} g")

    def test_validation_normal_values(self):
        """Verify that normal predictions within biological range are NOT adjusted."""
        # Mean weight is around 284.64 g, Q50 is 279 g
        normal_weights = [250.0, 279.0, 327.0, 380.0]
        
        for w in normal_weights:
            res = validate_prediction(w)
            self.assertFalse(res["was_adjusted"])
            self.assertEqual(res["original_prediction"], w)
            self.assertEqual(res["prediction_value"], w)
            self.assertEqual(res["validation_message"], "Valid prediction")

    def test_validation_boundary_values(self):
        """Verify that values exactly at the boundaries are NOT adjusted."""
        # Minimum realistic weight
        res_min = validate_prediction(MIN_WEIGHT)
        self.assertFalse(res_min["was_adjusted"])
        self.assertEqual(res_min["prediction_value"], MIN_WEIGHT)
        
        # Maximum realistic weight
        res_max = validate_prediction(MAX_WEIGHT)
        self.assertFalse(res_max["was_adjusted"])
        self.assertEqual(res_max["prediction_value"], MAX_WEIGHT)

    def test_validation_extreme_high_values(self):
        """Verify that values above the maximum are adjusted to the 95th percentile."""
        extreme_highs = [412.01, 500.0, 9440.0, 100000.0]
        
        for w in extreme_highs:
            res = validate_prediction(w)
            self.assertTrue(res["was_adjusted"])
            self.assertEqual(res["original_prediction"], round(w, 2))
            self.assertEqual(res["prediction_value"], round(P95_WEIGHT, 2))
            self.assertEqual(res["validation_message"], "Prediction was outside biological range and was corrected.")

    def test_validation_extreme_low_values(self):
        """Verify that values below the minimum are adjusted to the 5th percentile."""
        extreme_lows = [149.99, 100.0, 0.0, -50.0]
        
        for w in extreme_lows:
            res = validate_prediction(w)
            self.assertTrue(res["was_adjusted"])
            self.assertEqual(res["original_prediction"], round(w, 2))
            self.assertEqual(res["prediction_value"], round(P5_WEIGHT, 2))
            self.assertEqual(res["validation_message"], "Prediction was outside biological range and was corrected.")


class TestPredictionPipelineIntegration(unittest.TestCase):
    
    def setUp(self):
        # A normal/typical input scenario
        self.normal_inputs = {
            "air_temperature": 22.0,
            "humidity": 60.0,
            "co2": 450.0,
            "water_ph": 6.2,
            "water_ec": 2.0,
            "water_tds": 1.0,
            "water_temperature": 23.0,
            "nutrient_solution_ml": 400.0,
            "water_consumption_l": 170.0,
            "acid_consumption_ml": 40.0,
            "initial_height_cm": 12.0,
            "initial_weight_g": 4.0,
            "initial_root_length_cm": 7.0,
        }
        
        # Extreme input that forces high inputs (but mathematically yields raw prediction of 0.0 g due to LR coefficients extrapolation)
        self.extreme_high_inputs = {
            "air_temperature": 38.0,
            "humidity": 85.0,
            "co2": 1000.0,
            "water_ph": 8.5,
            "water_ec": 5.0,
            "water_tds": 3.0,
            "water_temperature": 35.0,
            "nutrient_solution_ml": 1500.0,
            "water_consumption_l": 500.0,
            "acid_consumption_ml": 200.0,
            "initial_height_cm": 20.0,
            "initial_weight_g": 10.0,
            "initial_root_length_cm": 15.0,
        }

        # Extreme input that forces low inputs (but mathematically yields raw prediction of 8771.68 g)
        self.extreme_low_inputs = {
            "air_temperature": 10.0,
            "humidity": 30.0,
            "co2": 300.0,
            "water_ph": 4.0,
            "water_ec": 0.5,
            "water_tds": 0.3,
            "water_temperature": 15.0,
            "nutrient_solution_ml": 0.0,
            "water_consumption_l": 0.0,
            "acid_consumption_ml": 0.0,
            "initial_height_cm": 5.0,
            "initial_weight_g": 0.5,
            "initial_root_length_cm": 3.0,
        }

    def test_pipeline_normal_prediction(self):
        """Verify normal prediction works without adjustments and returns all expected fields."""
        res = predict(self.normal_inputs)
        
        self.assertIn("predicted_weight", res)
        self.assertIn("growth_category", res)
        self.assertIn("prediction_value", res)
        self.assertIn("original_prediction", res)
        self.assertIn("was_adjusted", res)
        self.assertIn("validation_message", res)
        
        self.assertEqual(res["predicted_weight"], res["prediction_value"])
        self.assertFalse(res["was_adjusted"])
        self.assertEqual(res["validation_message"], "Valid prediction")
        
        # Clean terminal output (stripping emoji if python encoding fallback fails)
        cat_str = res['growth_category'].encode('ascii', errors='ignore').decode().strip()
        print(f"\n[INFO] Normal Prediction Integration Result:")
        print(f"  - Original weight: {res['original_prediction']} g")
        print(f"  - Validated weight: {res['prediction_value']} g")
        print(f"  - Category: {cat_str}")
        print(f"  - Was Adjusted: {res['was_adjusted']}")

    def test_pipeline_extreme_high_prediction(self):
        """Verify extreme inputs trigger validation and get clipped to P5_WEIGHT (since raw prediction is 0.0 g)."""
        res = predict(self.extreme_high_inputs)
        
        self.assertTrue(res["was_adjusted"])
        self.assertEqual(res["prediction_value"], round(P5_WEIGHT, 2))
        self.assertEqual(res["validation_message"], "Prediction was outside biological range and was corrected.")
        
        cat_str = res['growth_category'].encode('ascii', errors='ignore').decode().strip()
        print(f"\n[INFO] Extreme High Input Result (Adjusted to P5):")
        print(f"  - Original weight: {res['original_prediction']} g")
        print(f"  - Validated weight: {res['prediction_value']} g")
        print(f"  - Category: {cat_str}")
        print(f"  - Was Adjusted: {res['was_adjusted']}")

    def test_pipeline_extreme_low_prediction(self):
        """Verify extreme low inputs trigger validation and get clipped to P95_WEIGHT (since raw prediction is 8771.68 g)."""
        res = predict(self.extreme_low_inputs)
        
        self.assertTrue(res["was_adjusted"])
        self.assertEqual(res["prediction_value"], round(P95_WEIGHT, 2))
        self.assertEqual(res["validation_message"], "Prediction was outside biological range and was corrected.")
        
        cat_str = res['growth_category'].encode('ascii', errors='ignore').decode().strip()
        print(f"\n[INFO] Extreme Low Input Result (Adjusted to P95):")
        print(f"  - Original weight: {res['original_prediction']} g")
        print(f"  - Validated weight: {res['prediction_value']} g")
        print(f"  - Category: {cat_str}")
        print(f"  - Was Adjusted: {res['was_adjusted']}")


if __name__ == "__main__":
    unittest.main()
