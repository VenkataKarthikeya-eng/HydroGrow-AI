import unittest
from backend.services.ai_agents.nutrition_agent import NutritionAgent

class TestNutritionAgent(unittest.TestCase):

    def test_nutrition_agent_balanced(self):
        context = {
            "iot_info": {"water_ph": 6.2, "water_ec": 2.0, "nutrient_level": 85.0}
        }
        res = NutritionAgent.run(context)
        self.assertEqual(res["priority"], "LOW")

    def test_nutrition_agent_ph_drift(self):
        context = {
            "iot_info": {"water_ph": 4.5, "water_ec": 2.0, "nutrient_level": 85.0}
        }
        res = NutritionAgent.run(context)
        self.assertEqual(res["priority"], "CRITICAL")
        self.assertIn("Acidic pH drop", res["analysis"])

if __name__ == "__main__":
    unittest.main()
