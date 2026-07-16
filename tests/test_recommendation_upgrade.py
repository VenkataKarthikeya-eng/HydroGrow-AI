"""
test_recommendation_upgrade.py — Verification of Upgraded Recommendation Engine & Validation Layer

This test script validates the recommendation engine upgrade under:
1. Normal hydroponic conditions
2. Low pH conditions (Warning & Critical)
3. High temperature conditions (Warning & Critical)
4. Low CO2 conditions (Warning & Critical)
5. Verifies that the Phase 6.1 validation layer is still working alongside the recommendations.
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

from backend.services.intelligence.recommendation_engine import generate_recommendations
from backend.services.prediction.prediction import predict
from backend.services.prediction.prediction_validation import P5_WEIGHT, P95_WEIGHT


class TestRecommendationEngineUpgrade(unittest.TestCase):
    
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
        
        # Extreme inputs that force out of range prediction (0.0 g)
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

    def test_normal_conditions(self):
        """Verify that under optimal parameters, recommendations return 'success' (Optimal) cards."""
        recs = generate_recommendations(self.normal_inputs)
        
        # We expect all parameters to be in the optimal range
        print("\n[INFO] Running Normal Hydroponic Conditions Test...")
        for rec in recs:
            # Check structure
            self.assertEqual(rec["type"], "success")
            self.assertEqual(rec["status"], "Optimal")
            self.assertIn("parameter", rec)
            self.assertIn("value", rec)
            self.assertIn("message", rec)
            self.assertIn("action", rec)
            print(f"  - [{rec['status']}] {rec['parameter']}: {rec['value']} -> {rec['action']}")

    def test_low_ph_scenarios(self):
        """Verify that low pH levels trigger Warning and Critical recommendation cards."""
        print("\n[INFO] Running Low pH Scenarios Test...")
        
        # Test pH 5.2 (Warning)
        inputs_warning = self.normal_inputs.copy()
        inputs_warning["water_ph"] = 5.2
        recs_warning = generate_recommendations(inputs_warning)
        ph_rec = next(r for r in recs_warning if r["parameter"] == "Water pH")
        self.assertEqual(ph_rec["type"], "warning")
        self.assertEqual(ph_rec["status"], "Warning")
        self.assertIn("calcium and magnesium", ph_rec["message"])
        print(f"  - [Warning pH 5.2]: status: {ph_rec['status']}, explanation: {ph_rec['message']}, action: {ph_rec['action']}")
        
        # Test pH 4.5 (Critical)
        inputs_critical = self.normal_inputs.copy()
        inputs_critical["water_ph"] = 4.5
        recs_critical = generate_recommendations(inputs_critical)
        ph_rec_crit = next(r for r in recs_critical if r["parameter"] == "Water pH")
        self.assertEqual(ph_rec_crit["type"], "critical")
        self.assertEqual(ph_rec_crit["status"], "Critical")
        self.assertIn("root burn", ph_rec_crit["message"])
        print(f"  - [Critical pH 4.5]: status: {ph_rec_crit['status']}, explanation: {ph_rec_crit['message']}, action: {ph_rec_crit['action']}")

    def test_high_temperature_scenarios(self):
        """Verify that high temperatures trigger Warning and Critical recommendation cards."""
        print("\n[INFO] Running High Temperature Scenarios Test...")
        
        # Test Air Temperature 26.0 °C (Warning) and Water Temperature 25.0 °C (Warning)
        inputs_warning = self.normal_inputs.copy()
        inputs_warning["air_temperature"] = 26.0
        inputs_warning["water_temperature"] = 25.0
        recs_warning = generate_recommendations(inputs_warning)
        
        air_rec = next(r for r in recs_warning if r["parameter"] == "Air Temperature")
        self.assertEqual(air_rec["type"], "warning")
        self.assertEqual(air_rec["status"], "Warning")
        print(f"  - [Warning Air Temp 26.0°C]: status: {air_rec['status']}, action: {air_rec['action']}")
        
        water_rec = next(r for r in recs_warning if r["parameter"] == "Water Temperature")
        self.assertEqual(water_rec["type"], "warning")
        self.assertEqual(water_rec["status"], "Warning")
        print(f"  - [Warning Water Temp 25.0°C]: status: {water_rec['status']}, action: {water_rec['action']}")
        
        # Test Air Temperature 31.0 °C (Critical) and Water Temperature 28.0 °C (Critical)
        inputs_critical = self.normal_inputs.copy()
        inputs_critical["air_temperature"] = 31.0
        inputs_critical["water_temperature"] = 28.0
        recs_critical = generate_recommendations(inputs_critical)
        
        air_rec_crit = next(r for r in recs_critical if r["parameter"] == "Air Temperature")
        self.assertEqual(air_rec_crit["type"], "critical")
        self.assertEqual(air_rec_crit["status"], "Critical")
        print(f"  - [Critical Air Temp 31.0°C]: status: {air_rec_crit['status']}, action: {air_rec_crit['action']}")
        
        water_rec_crit = next(r for r in recs_critical if r["parameter"] == "Water Temperature")
        self.assertEqual(water_rec_crit["type"], "critical")
        self.assertEqual(water_rec_crit["status"], "Critical")
        print(f"  - [Critical Water Temp 28.0°C]: status: {water_rec_crit['status']}, action: {water_rec_crit['action']}")

    def test_low_co2_scenarios(self):
        """Verify that low CO2 levels trigger Warning and Critical recommendation cards."""
        print("\n[INFO] Running Low CO2 Scenarios Test...")
        
        # Test CO2 350 ppm (Warning)
        inputs_warning = self.normal_inputs.copy()
        inputs_warning["co2"] = 350.0
        recs_warning = generate_recommendations(inputs_warning)
        co2_rec = next(r for r in recs_warning if r["parameter"] == "CO2 Level")
        self.assertEqual(co2_rec["type"], "warning")
        self.assertEqual(co2_rec["status"], "Warning")
        print(f"  - [Warning CO2 350 ppm]: status: {co2_rec['status']}, action: {co2_rec['action']}")
        
        # Test CO2 280 ppm (Critical)
        inputs_critical = self.normal_inputs.copy()
        inputs_critical["co2"] = 280.0
        recs_critical = generate_recommendations(inputs_critical)
        co2_rec_crit = next(r for r in recs_critical if r["parameter"] == "CO2 Level")
        self.assertEqual(co2_rec_crit["type"], "critical")
        self.assertEqual(co2_rec_crit["status"], "Critical")
        print(f"  - [Critical CO2 280 ppm]: status: {co2_rec_crit['status']}, action: {co2_rec_crit['action']}")

    def test_phase_6_1_validation_compatibility(self):
        """Verify that Phase 6.1 validation layer still functions alongside updated recommendations."""
        print("\n[INFO] Testing Phase 6.1 Validation Compatibility...")
        
        # Normal inputs should yield a valid prediction (around 189.38 g, not adjusted)
        res_normal = predict(self.normal_inputs)
        self.assertFalse(res_normal["was_adjusted"])
        self.assertEqual(res_normal["validation_message"], "Valid prediction")
        print(f"  - [Normal Inputs Validation]: adjusted: {res_normal['was_adjusted']}, value: {res_normal['prediction_value']} g")
        
        # Extreme inputs should generate 0.0g raw model prediction, clipped to P5 (201.5 g)
        res_extreme = predict(self.extreme_high_inputs)
        self.assertTrue(res_extreme["was_adjusted"])
        self.assertEqual(res_extreme["prediction_value"], round(P5_WEIGHT, 2))
        print(f"  - [Extreme Inputs Validation]: adjusted: {res_extreme['was_adjusted']}, value: {res_extreme['prediction_value']} g (Clipped to P5)")


if __name__ == "__main__":
    unittest.main()
