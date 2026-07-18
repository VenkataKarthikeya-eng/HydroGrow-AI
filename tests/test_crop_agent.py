import unittest
from backend.services.ai_agents.crop_agent import CropAgent

class TestCropAgent(unittest.TestCase):

    def test_crop_agent_normal(self):
        context = {
            "crop_info": {"current_stage": "Vegetative", "growth_progress": 65.0, "days_remaining": 10},
            "vision_info": {"health_score": 95.0}
        }
        res = CropAgent.run(context)
        self.assertEqual(res["agent_name"], "CropAgent")
        self.assertEqual(res["priority"], "LOW")

    def test_crop_agent_slow_growth(self):
        context = {
            "crop_info": {"current_stage": "Maturity", "growth_progress": 30.0, "days_remaining": 2},
            "vision_info": {"health_score": 85.0}
        }
        res = CropAgent.run(context)
        self.assertEqual(res["priority"], "HIGH")
        self.assertIn("Slow growth detected", res["analysis"])

if __name__ == "__main__":
    unittest.main()
