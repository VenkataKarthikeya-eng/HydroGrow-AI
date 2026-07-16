"""
test_explanation_engine.py — Unit Tests for Prediction Explanation Engine

This test script validates the explanation engine:
1. Normal optimal inputs generate positive explanations and no improvement opportunities.
2. Poor growing conditions generate correct improvement opportunities (e.g. low pH, low CO2).
3. Returned dictionary follows the correct schema.
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

from backend.services.intelligence.explanation_engine import generate_explanation
from backend.services.intelligence.recommendation_engine import generate_recommendations
from backend.services.prediction.prediction import predict


class TestExplanationEngine(unittest.TestCase):
    
    def setUp(self):
        # Baseline normal conditions
        self.normal_inputs = {
            "air_temperature": 22.0,
            "humidity": 60.0,
            "co2": 450.0,
            "water_ph": 6.2,
            "water_ec": 2.0,
            "water_tds": 1.0,
            "water_temperature": 21.0,
            "nutrient_solution_ml": 400.0,
            "water_consumption_l": 170.0,
            "acid_consumption_ml": 40.0,
            "initial_height_cm": 12.0,
            "initial_weight_g": 4.0,
            "initial_root_length_cm": 7.0,
        }
        
        # Poor conditions: Low pH (4.5 - critical), low CO2 (350 - warning)
        self.poor_inputs = {
            "air_temperature": 22.0,
            "humidity": 60.0,
            "co2": 350.0,                  # Warning low CO2
            "water_ph": 4.5,               # Critical low pH
            "water_ec": 2.0,
            "water_tds": 1.0,
            "water_temperature": 21.0,
            "nutrient_solution_ml": 400.0,
            "water_consumption_l": 170.0,
            "acid_consumption_ml": 40.0,
            "initial_height_cm": 12.0,
            "initial_weight_g": 4.0,
            "initial_root_length_cm": 7.0,
        }

    def test_output_format(self):
        """Verify that generate_explanation returns a dictionary with the correct keys and types."""
        pred_res = predict(self.normal_inputs)
        recs = generate_recommendations(self.normal_inputs)
        explanation = generate_explanation(self.normal_inputs, pred_res, recs)
        
        self.assertIsInstance(explanation, dict)
        self.assertIn("summary", explanation)
        self.assertIn("positive_factors", explanation)
        self.assertIn("improvement_opportunities", explanation)
        self.assertIn("confidence_explanation", explanation)
        
        self.assertIsInstance(explanation["summary"], str)
        self.assertIsInstance(explanation["positive_factors"], list)
        self.assertIsInstance(explanation["improvement_opportunities"], list)
        self.assertIsInstance(explanation["confidence_explanation"], str)

    def test_normal_optimal_inputs(self):
        """Verify that optimal inputs produce positive factors and no improvement opportunities."""
        pred_res = predict(self.normal_inputs)
        recs = generate_recommendations(self.normal_inputs)
        explanation = generate_explanation(self.normal_inputs, pred_res, recs)
        
        # All 11 parameters in setup are optimal
        self.assertEqual(len(explanation["positive_factors"]), 11)
        self.assertEqual(len(explanation["improvement_opportunities"]), 0)
        
        # Check a few specific optimal factors
        ph_factor = next(f for f in explanation["positive_factors"] if f["factor"] == "Water pH")
        self.assertEqual(ph_factor["impact"], "positive")
        self.assertIn("optimal and supports nutrient absorption", ph_factor["explanation"])
        
        co2_factor = next(f for f in explanation["positive_factors"] if f["factor"] == "CO2 Level")
        self.assertEqual(co2_factor["impact"], "positive")
        self.assertIn("CO2 level (450 ppm) is productive", co2_factor["explanation"])
        
        # Strip emoji for printing safely
        summary_clean = explanation['summary'].encode('ascii', errors='ignore').decode().strip()
        print("\n[INFO] Normal Optimal Inputs Test Passed:")
        print(f"  - Summary: {summary_clean}")
        print(f"  - Positive factors count: {len(explanation['positive_factors'])}")
        print(f"  - Improvement opportunities count: {len(explanation['improvement_opportunities'])}")

    def test_poor_conditions(self):
        """Verify that poor growing parameters correctly populate improvement opportunities."""
        pred_res = predict(self.poor_inputs)
        recs = generate_recommendations(self.poor_inputs)
        explanation = generate_explanation(self.poor_inputs, pred_res, recs)
        
        # We expect Water pH and CO2 Level to be in improvement opportunities, the other 9 in positive factors
        self.assertEqual(len(explanation["positive_factors"]), 9)
        self.assertEqual(len(explanation["improvement_opportunities"]), 2)
        
        # Validate pH opportunity (pH 4.5 is critical low)
        ph_opp = next(f for f in explanation["improvement_opportunities"] if f["factor"] == "Water pH")
        self.assertEqual(ph_opp["impact"], "improvement")
        self.assertIn("Water pH (4.5) is critically low", ph_opp["explanation"])
        self.assertIn("root damage", ph_opp["explanation"])
        
        # Validate CO2 opportunity (CO2 350 is warning low)
        co2_opp = next(f for f in explanation["improvement_opportunities"] if f["factor"] == "CO2 Level")
        self.assertEqual(co2_opp["impact"], "improvement")
        self.assertIn("CO2 level is below the ideal productivity range", co2_opp["explanation"])
        
        # Strip emoji for printing safely
        summary_clean = explanation['summary'].encode('ascii', errors='ignore').decode().strip()
        print("\n[INFO] Poor Conditions Test Passed:")
        print(f"  - Summary: {summary_clean}")
        print(f"  - Opportunities identified:")
        for opp in explanation["improvement_opportunities"]:
            opp_clean = opp['explanation'].encode('ascii', errors='ignore').decode().strip()
            print(f"    * {opp['factor']}: {opp_clean}")


if __name__ == "__main__":
    unittest.main()
