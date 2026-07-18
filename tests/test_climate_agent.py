import unittest
from backend.services.ai_agents.climate_agent import ClimateAgent

class TestClimateAgent(unittest.TestCase):

    def test_climate_agent_optimal(self):
        context = {
            "iot_info": {"temperature": 22.0, "humidity": 60.0, "co2": 450.0, "water_temperature": 21.0}
        }
        res = ClimateAgent.run(context)
        self.assertEqual(res["priority"], "LOW")

    def test_climate_agent_heat_stress(self):
        context = {
            "iot_info": {"temperature": 32.0, "humidity": 60.0, "co2": 450.0, "water_temperature": 21.0}
        }
        res = ClimateAgent.run(context)
        self.assertEqual(res["priority"], "CRITICAL")
        self.assertIn("Heat stress", res["analysis"])

if __name__ == "__main__":
    unittest.main()
