import unittest
from backend.services.vision.disease_detector import DiseaseDetector

class TestDiseaseDetection(unittest.TestCase):
    def test_classify_healthy(self):
        res = DiseaseDetector().predict("lettuce_healthy.png")
        self.assertEqual(res["disease"], "Healthy")
        self.assertEqual(res["severity"], "None")

    def test_classify_tipburn(self):
        res = DiseaseDetector().predict("lettuce_tipburn.png")
        self.assertEqual(res["disease"], "Tip Burn")
        self.assertEqual(res["severity"], "Medium")

    def test_classify_deficiency(self):
        res = DiseaseDetector().predict("deficiency_symptom.jpg")
        self.assertEqual(res["disease"], "Nutrient Deficiency")
        self.assertEqual(res["severity"], "Low")
