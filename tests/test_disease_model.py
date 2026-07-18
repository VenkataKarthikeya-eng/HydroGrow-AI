import unittest
from backend.ml.models.disease_model import DiseaseModel

class TestDiseaseModel(unittest.TestCase):

    def test_predict_disease_healthy(self):
        dm = DiseaseModel()
        res = dm.predict_disease(filename="healthy_lettuce.jpg")
        self.assertEqual(res["disease_name"], "Healthy")
        self.assertGreaterEqual(res["confidence_score"], 90.0)

    def test_predict_disease_tip_burn(self):
        dm = DiseaseModel()
        res = dm.predict_disease(filename="tip_burn_scan.jpg")
        self.assertEqual(res["disease_name"], "Tip Burn")
        self.assertEqual(res["severity"], "High")

if __name__ == "__main__":
    unittest.main()
