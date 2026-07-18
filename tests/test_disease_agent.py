import unittest
from backend.services.ai_agents.disease_agent import DiseaseAgent

class TestDiseaseAgent(unittest.TestCase):

    def test_disease_agent_healthy(self):
        context = {
            "vision_info": {"disease": "Healthy", "confidence": 0.98, "severity": "Low"}
        }
        res = DiseaseAgent.run(context)
        self.assertEqual(res["priority"], "LOW")

    def test_disease_agent_tip_burn(self):
        context = {
            "vision_info": {"disease": "Tip Burn", "confidence": 0.92, "severity": "High"}
        }
        res = DiseaseAgent.run(context)
        self.assertEqual(res["priority"], "HIGH")
        self.assertIn("Tip Burn", res["analysis"])

if __name__ == "__main__":
    unittest.main()
