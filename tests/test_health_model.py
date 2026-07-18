import unittest
from backend.ml.models.health_model import HealthModel

class TestHealthModel(unittest.TestCase):

    def test_calculate_health_score(self):
        v = {"health_score": 95.0}
        iot = {"temperature": 22.0, "water_ph": 6.2, "water_ec": 2.0}
        growth = {"fresh_weight": 310.0}

        score = HealthModel.calculate_health_score(v, iot, growth)
        self.assertEqual(score, 100.0)

if __name__ == "__main__":
    unittest.main()
