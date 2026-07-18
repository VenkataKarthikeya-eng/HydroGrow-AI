import unittest
from backend.services.digital_twin.growth_simulator import GrowthSimulator

class TestGrowthSimulator(unittest.TestCase):
    def test_get_stage_for_day(self):
        self.assertEqual(GrowthSimulator.get_stage_for_day(5), "Seedling")
        self.assertEqual(GrowthSimulator.get_stage_for_day(15), "Vegetative")
        self.assertEqual(GrowthSimulator.get_stage_for_day(30), "Maturity")
        self.assertEqual(GrowthSimulator.get_stage_for_day(40), "Harvest")

    def test_calculate_daily_state_optimal(self):
        # Optimal: temp=22, water_ec=2.0
        state = GrowthSimulator.calculate_daily_state(15, {
            "temperature": 22.0,
            "humidity": 60.0,
            "co2": 450.0,
            "water_ec": 2.0,
            "water_ph": 6.0,
            "light_hours": 16.0
        })
        self.assertEqual(state["growth_stage"], "Vegetative")
        self.assertGreater(state["predicted_weight"], 10.0)
        self.assertEqual(state["health_score"], 100.0)

    def test_calculate_daily_state_stress(self):
        # High heat and high EC stress
        state = GrowthSimulator.calculate_daily_state(30, {
            "temperature": 32.0,
            "humidity": 60.0,
            "co2": 450.0,
            "water_ec": 3.2,
            "water_ph": 6.0,
            "light_hours": 16.0
        })
        self.assertEqual(state["growth_stage"], "Maturity")
        self.assertLess(state["health_score"], 80.0)
