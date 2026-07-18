import unittest
from backend.services.digital_twin.scenario_engine import ScenarioEngine

class TestScenarioEngine(unittest.TestCase):
    def test_run_scenario_comparison_improvement(self):
        # Base hot vs modified optimal
        base = {"temperature": 30.0, "water_ec": 2.8}
        mod = {"temperature": 22.0, "water_ec": 2.0}
        
        res = ScenarioEngine.run_scenario_comparison(base, mod, duration_days=30)
        self.assertGreater(res["yield_change_percentage"], 0.0)
        self.assertIn("positive yield improvement", res["recommendations"][0].lower())

    def test_run_scenario_comparison_reduction(self):
        # Base optimal vs modified extreme stress
        base = {"temperature": 22.0, "water_ec": 2.0}
        mod = {"temperature": 34.0, "water_ec": 3.4}
        
        res = ScenarioEngine.run_scenario_comparison(base, mod, duration_days=30)
        self.assertLess(res["yield_change_percentage"], 0.0)
        self.assertIn("reduce yield", res["recommendations"][0].lower())
