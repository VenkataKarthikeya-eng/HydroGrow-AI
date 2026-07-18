import unittest
from backend.services.digital_twin.forecast_engine import ForecastEngine

class TestForecastEngine(unittest.TestCase):
    def test_generate_growth_forecast_optimal(self):
        conds = {
            "temperature": 22.0,
            "humidity": 60.0,
            "co2": 450.0,
            "water_ec": 2.0,
            "water_ph": 6.0,
            "light_hours": 16.0
        }
        res = ForecastEngine.generate_growth_forecast(conds, duration_days=35)
        self.assertEqual(len(res["growth_forecast"]), 35)
        self.assertEqual(res["confidence_score"], 0.95)
        self.assertEqual(len(res["risk_factors"]), 0)

    def test_generate_growth_forecast_stresses(self):
        conds = {
            "temperature": 30.0,
            "humidity": 60.0,
            "co2": 450.0,
            "water_ec": 3.0,
            "water_ph": 6.0,
            "light_hours": 16.0
        }
        res = ForecastEngine.generate_growth_forecast(conds, duration_days=35)
        self.assertLess(res["confidence_score"], 0.90)
        self.assertGreater(len(res["risk_factors"]), 0)
